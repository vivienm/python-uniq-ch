use std::hash::{BuildHasher, BuildHasherDefault, Hash};

use highway::HighwayHasher;
use pyo3::{
    exceptions::{PyRuntimeError, PyTypeError, PyValueError},
    prelude::*,
    types::{PyBytes, PyInt, PyString},
};

#[pyclass(name = "BJKST")]
struct Bjkst {
    inner: uniq_ch::Bjkst<(), BuildHasherDefault<HighwayHasher>>,
}

impl Bjkst {
    fn hash_generic<T>(&self, value: T) -> u64
    where
        T: Hash,
    {
        self.inner.hasher().hash_one(&value)
    }
}

#[pymethods]
impl Bjkst {
    #[new]
    fn new(py: Python, precision: u8) -> PyResult<Self> {
        py.allow_threads(|| {
            let precision = uniq_ch::Precision::new(precision).ok_or_else(|| {
                PyValueError::new_err(format!("Invalid precision: {}", precision))
            })?;
            Ok(Bjkst {
                inner: uniq_ch::Bjkst::with_precision(precision),
            })
        })
    }

    fn __bool__(&self, py: Python) -> bool {
        py.allow_threads(|| !self.inner.is_empty())
    }

    fn __len__(&self, py: Python) -> usize {
        py.allow_threads(|| self.inner.len())
    }

    fn add(&mut self, py: Python, value: &Bound<'_, PyAny>) -> PyResult<()> {
        let hash = self.hash(py, value)?;
        self.add_hash(py, hash);
        Ok(())
    }

    fn add_hash(&mut self, py: Python, hash: u64) {
        py.allow_threads(|| self.inner.insert_hash(hash));
    }

    fn clear(&mut self, py: Python) {
        py.allow_threads(|| self.inner.clear())
    }

    fn copy(&self, py: Python) -> Self {
        py.allow_threads(|| Self {
            inner: self.inner.clone(),
        })
    }

    #[staticmethod]
    fn deserialize(py: Python, data: &[u8]) -> PyResult<Self> {
        py.allow_threads(|| {
            let inner: uniq_ch::Bjkst<(), _> = bincode::deserialize(data).map_err(|e| {
                PyValueError::new_err(format!("Failed to deserialize BJKST: {}", e))
            })?;
            Ok(Self { inner })
        })
    }

    fn hash(&self, py: Python, value: &Bound<'_, PyAny>) -> PyResult<u64> {
        Ok(if let Ok(value) = value.downcast::<PyInt>() {
            let value: i128 = value.extract()?;
            py.allow_threads(|| self.hash_generic(value))
        } else if let Ok(value) = value.downcast::<PyBytes>() {
            let value: &[u8] = value.as_bytes();
            py.allow_threads(|| self.hash_generic(value))
        } else if let Ok(value) = value.downcast::<PyString>() {
            let value = value.to_str()?;
            py.allow_threads(|| self.hash_generic(value))
        } else {
            Err(PyTypeError::new_err(format!(
                "unsupported type: {}",
                value
                    .get_type()
                    .name()
                    .map_or_else(|_| "{unknown}".into(), |name| name.to_string())
            )))?
        })
    }

    fn serialize(&self, py: Python) -> PyResult<PyObject> {
        let data = py.allow_threads(|| {
            bincode::serialize(&self.inner)
                .map_err(|e| PyRuntimeError::new_err(format!("Failed to serialize BJKST: {}", e)))
        })?;
        Ok(PyBytes::new_bound(py, &data).into())
    }

    fn update_bjkst(&mut self, py: Python, other: &Self) {
        py.allow_threads(|| self.inner |= &other.inner)
    }

    fn update_hashes(&mut self, py: Python, hashes: Vec<u64>) {
        py.allow_threads(|| {
            for hash in hashes {
                self.inner.insert_hash(hash);
            }
        })
    }
}

/// Low-level extension module.
#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Bjkst>()?;
    Ok(())
}
