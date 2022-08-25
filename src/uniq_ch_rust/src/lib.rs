use std::hash::{BuildHasher, BuildHasherDefault, Hash, Hasher};

use highway::HighwayHasher;
use pyo3::{
    exceptions::PyTypeError,
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
        let mut hasher = self.inner.hasher().build_hasher();
        value.hash(&mut hasher);
        hasher.finish()
    }
}

#[pymethods]
impl Bjkst {
    #[new]
    fn new(py: Python) -> Self {
        py.allow_threads(|| Bjkst {
            inner: uniq_ch::Bjkst::default(),
        })
    }

    fn __bool__(&self, py: Python) -> bool {
        py.allow_threads(|| !self.inner.is_empty())
    }

    fn __len__(&self, py: Python) -> usize {
        py.allow_threads(|| self.inner.len())
    }

    fn add(&mut self, py: Python, value: &PyAny) -> PyResult<()> {
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

    fn hash(&self, py: Python, value: &PyAny) -> PyResult<u64> {
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
                value.get_type().name().unwrap_or("{unknown}")
            )))?
        })
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

#[pymodule]
fn uniq_ch_rust(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<Bjkst>()?;
    Ok(())
}
