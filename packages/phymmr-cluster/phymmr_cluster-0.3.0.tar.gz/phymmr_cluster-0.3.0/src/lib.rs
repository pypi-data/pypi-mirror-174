#![allow(unused, unused_mut)]

use std::path::PathBuf;

use pyo3::prelude::*;
use itertools::*;
use hashbrown::HashMap;
use std::io;
use std::fs::File;


trait Hash {
    fn to_map(&self) -> HashMap<String, Vec<(Vec<u8>, (String, String))>>;
 }

 impl Hash for [(String, Vec<u8>, String, String)] {
    fn to_map(&self) -> HashMap<String, Vec<(Vec<u8>, (String, String))>> {
       let mut hm = HashMap::new();

       self
        .iter()
        .cloned()
        .for_each(|(k ,v1, v2, v3)| {
            hm
                .entry(k)
                .or_insert(
                    Vec::new()
                ).push(
                    (
                        v1, 
                        (
                            v2, 
                            v3
                        )
                    )
                );
        });

        hm
    }
 }

#[pyfunction]
fn read_fasta_get_clusters(records: Vec<(String, String)>, limit: usize) -> Vec<Vec<(Vec<u8>, (String, String))>> {
    let seqs_clusters = records
                .iter()
                .cloned()
                .map(|(header, seq)| {
                    let limit_lead = seq[0..limit].to_owned();
                    let seq_bytes = seq.as_bytes().to_vec();

                    (limit_lead, seq_bytes, header, seq)
                })
                .collect::<Vec<_>>()
                .to_map();


    seqs_clusters.into_values().collect_vec()         
}

#[pyfunction]
fn get_max_and_pad(cluster: Vec<Vec<u8>>) -> (Vec<Vec<u8>>, usize, usize) {
    let max: usize = cluster
                        .iter()
                        .cloned()
                        .map(|x| x.len())
                        .max()
                        .unwrap();

    let padded = cluster
                        .iter()
                        .cloned()
                        .map(|mut x| {
                            x.extend(vec![0; max - x.len()]);
                            x
                        })
                        .collect::<Vec<_>>();

    
    (padded, cluster.len(), max)
}


#[pymodule]
fn phymmr_cluster(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(read_fasta_get_clusters, m)?)?;
    m.add_function(wrap_pyfunction!(get_max_and_pad, m)?)?;

    Ok(())
}
