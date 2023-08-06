use std::{fmt::Debug, hash::Hash, mem, rc::Rc, sync::Arc};

use macro_rules_attribute::apply;
use once_cell::sync::Lazy;
use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet};

use crate::make_lazy;
pub type AxisInt = u8;

/// letters used in einsum and rearrange strings
/// i wanted this to be a constant, but that is annoying in rust bc can't do any computation to produce constants
/// so instead it's cached function
#[apply(make_lazy)]
#[lazy_ty(Lazy)]
pub fn alphabet() -> Vec<String> {
    let alphabet_upper: Vec<String> = ('A'..'[').map(|x| x.to_string()).collect(); // char after Z
    let alphabet_lower: Vec<String> = ('a'..'{').map(|x| x.to_string()).collect();
    let alphabet_greek_lower: Vec<String> = ('α'..'ω').map(|x| x.to_string()).collect();
    let result = alphabet_lower
        .iter()
        .chain(alphabet_upper.iter())
        .chain(alphabet_greek_lower.iter())
        .cloned()
        .collect();
    result
}

#[apply(make_lazy)]
#[lazy_ty(Lazy)]
pub fn alphabet_inv() -> HashMap<String, usize> {
    ALPHABET
        .iter()
        .cloned()
        .enumerate()
        .map(|(a, b)| (b, a))
        .collect()
}

pub fn is_unique<T: Eq + Hash>(col: &[T]) -> bool {
    let set: HashSet<&T> = col.iter().collect();
    col.len() == set.len()
}

pub fn unique_to_appearance<T: Eq + Hash + Clone>(vec: &Vec<T>) -> HashMap<T, Vec<usize>> {
    let mut map: HashMap<T, Vec<usize>> = HashMap::default();
    for (i, x) in vec.iter().enumerate() {
        map.entry(x.clone()).or_insert(vec![]).push(i);
    }
    map
}

pub fn filter_to_idx<T>(col: &Vec<T>, f: &dyn Fn(&T) -> bool) -> Vec<usize> {
    col.iter()
        .enumerate()
        .filter(|(_i, x)| f(x))
        .map(|(i, _x)| i)
        .collect()
}

pub fn filter_out_idx<T: Clone>(col: &[T], idxs: &HashSet<usize>) -> Vec<T> {
    col.iter()
        .enumerate()
        .filter(|(i, _x)| !idxs.contains(i))
        .map(|(_i, x)| x)
        .cloned()
        .collect()
}

pub fn intersection_all<T: Eq + Hash + Copy>(sets: &Vec<HashSet<T>>) -> HashSet<T> {
    if sets.is_empty() {
        return HashSet::default();
    }
    let (first, rest) = sets.split_first().unwrap();
    rest.iter().fold(first.clone(), |acc, new| {
        acc.intersection(new).copied().collect()
    })
}

pub fn inverse_permutation(perm: &Vec<usize>) -> Vec<usize> {
    let mut result = vec![0; perm.len()];
    for (i, x) in perm.iter().enumerate() {
        result[*x] = i;
    }
    result
}

/// element at k in vec is v, max
pub fn dict_to_list(dict: &HashMap<usize, usize>, max: Option<usize>) -> Vec<usize> {
    let max = max.unwrap_or(*dict.keys().max().unwrap_or(&0));
    let mut result = vec![0; max + 1];
    for (k, v) in dict.iter() {
        result[*k] = *v;
    }
    result
}

/// Convenience function for managing a hashmap of vecs
pub fn vec_map_insert<T: Eq + Hash>(map: &mut HashMap<T, Vec<T>>, k: T, v: T) {
    map.entry(k).or_insert_with(Vec::new).push(v);
}

// wow this is a badly written macro. I'd really expect something like this to already exist
#[macro_export]
macro_rules! filter_by_variant {
    ($iterator:expr, $enum_name:ident, $variant:ident, $return_type:ty) => {{
        let mut yes: Vec<$return_type> = vec![];
        let mut no = vec![];
        for x in $iterator {
            match &*x {
                $enum_name::$variant(inner) => yes.push(inner.clone()),
                _ => no.push(x),
            }
        }
        (yes, no)
    }};
}

#[macro_export]
macro_rules! unwrap {
    ($target: expr, $pat: path) => {{
        if let $pat(a) = $target {
            // #1
            a
        } else {
            panic!("mismatch variant when cast to {}", stringify!($pat)); // #2
        }
    }};
}

#[macro_export]
macro_rules! timed {
    ($x:expr) => {{
        let timed_macro_now = std::time::Instant::now();

        let result = $x;

        let elapsed = timed_macro_now.elapsed();
        crate::python_println!("{} took {:.2?}", stringify!($x), elapsed);
        result
    }};
    ($x:expr,$min_to_print_milis:expr,$for_real:expr) => {{
        let timed_macro_now = std::time::Instant::now();

        let result = $x;

        let elapsed = timed_macro_now.elapsed();
        if $for_real && elapsed > std::time::Duration::new(0, $min_to_print_milis * 1_000_000) {
            crate::python_println!("{} took {:.2?}", stringify!($x), elapsed);
        }
        result
    }};
}
#[macro_export]
macro_rules! timed_value {
    ($x:expr) => {{
        let timed_macro_now = std::time::Instant::now();

        let result = $x;

        let elapsed = timed_macro_now.elapsed();
        (result, elapsed)
    }};
}

pub trait AsOp<T> {
    fn into_op(self) -> Option<T>
    where
        Self: Sized;
    fn as_op(&self) -> Option<&T>;
    fn as_mut_op(&mut self) -> Option<&mut T>;

    fn into_unwrap(self) -> T
    where
        Self: Sized,
    {
        self.into_op().unwrap()
    }
    fn as_unwrap(&self) -> &T {
        self.as_op().unwrap()
    }
    fn as_mut_unwrap(&mut self) -> &mut T {
        self.as_mut_op().unwrap()
    }

    fn map_or_clone<'a, F, O, OF>(&'a self, f: F) -> O
    where
        Self: Into<O>,
        OF: Into<O>,
        T: 'a,
        Self: Clone,
        F: FnOnce(&'a T) -> OF,
    {
        self.and_then_or_clone(|x| Some(f(x)))
    }
    fn and_then_or_clone<'a, F, O, OF>(&'a self, f: F) -> O
    where
        Self: Into<O>,
        OF: Into<O>,
        T: 'a,
        Self: Clone,
        F: FnOnce(&'a T) -> Option<OF>,
    {
        self.as_op()
            .and_then(f)
            .map(Into::into)
            .unwrap_or_else(|| self.clone().into())
    }
}

impl<T> AsOp<T> for T {
    fn into_op(self) -> Option<T> {
        Some(self)
    }
    fn as_op(&self) -> Option<&T> {
        Some(self)
    }
    fn as_mut_op(&mut self) -> Option<&mut T> {
        Some(self)
    }
}

pub fn mapping_until_end<T: Eq + Hash + Clone>(x: &T, mapping: &HashMap<T, T>) -> T {
    let mut result = x.clone();
    for _ in 0..1000 {
        match mapping.get(&result) {
            None => {
                return result;
            }
            Some(next) => {
                result = next.clone();
            }
        }
    }
    panic!("mapping_until_end didnt finish");
}

pub fn apply_fn_until_same<T: Eq + Hash + Clone + Debug, F>(x: &T, f: F) -> T
where
    F: FnMut(&T) -> T,
{
    let mut f = f;
    let mut result = x.clone();
    for i in 0..1000 {
        let next = f(&result);
        if next == result {
            return result;
        }
        result = next;
        if i == 1000 - 1 {
            dbg!(&result);
            panic!("apply until same didnt finish");
        }
    }
    result
}

pub fn apply_fn_until_none<T: Clone + Debug, F>(x: &T, f: F) -> T
where
    F: FnMut(&T) -> Option<T>,
{
    let mut f = f;
    let mut result = x.clone();
    for i in 0..1000 {
        match f(&result) {
            None => return result,
            Some(new) => result = new,
        }
        if i == 1000 - 1 {
            dbg!(&result);
            panic!("apply until none didnt finish");
        }
    }
    result
}

// might be fun to make memcpy based optimized outer product where we just copy blocks into place
pub fn outer_product<T: Clone>(cols: &Vec<Vec<T>>) -> Vec<Vec<T>> {
    assert!(!cols.iter().any(|x| x.is_empty()));
    if cols.is_empty() {
        return vec![vec![]];
    }

    let mut result: Vec<Vec<T>> = Vec::with_capacity(cols.iter().map(|x| x.len()).product());
    let mut places: Vec<usize> = vec![0; cols.len()];
    loop {
        result.push(
            places
                .iter()
                .enumerate()
                .map(|(i, place)| cols[i][*place].clone())
                .collect(),
        );

        let mut moving_place = cols.len() - 1;
        loop {
            places[moving_place] += 1;
            if places[moving_place] == cols[moving_place].len() {
                places[moving_place] = 0;
                if moving_place == 0 {
                    return result;
                }
                moving_place -= 1;
            } else {
                break;
            }
        }
    }
}

#[test]
pub fn test_outer_product() {
    let ex = vec![vec![0, 1], vec![2, 3, 4]];
    dbg!(outer_product(&ex));
}

// note this adds an element at the end so you can always look up arr[i+1] to get end
pub fn cumsum<T: std::ops::AddAssign + Default + Copy>(col: &[T]) -> Vec<T> {
    col.iter()
        .chain(std::iter::once(&Default::default()))
        .scan(Default::default(), |state: &mut T, el| {
            let old_state = *state;
            *state += *el;
            Some(old_state)
        })
        .collect()
}

pub fn hashmap_collect_except_duplicates<K: Eq + Hash + Clone, V: Eq + Hash + Clone>(
    it: impl Iterator<Item = (K, V)>,
) -> HashMap<K, V> {
    let mut result = HashMap::default();
    let mut dead: HashSet<K> = HashSet::default();
    for (k, v) in it {
        if !dead.contains(&k) {
            if let Some(old) = result.insert(k.clone(), v.clone()) {
                if old != v {
                    result.remove(&k);
                    dead.insert(k);
                }
            }
        }
    }
    result
}

pub type BitMask64 = usize;
pub type BitMask128 = u128;

#[macro_export]
macro_rules! ss {
    ($s:literal) => {
        Some($s.to_owned())
    };
}

/// this exists bc cursed jupyter bug that makes prints from rust hang
#[macro_export]
macro_rules! python_println{
    ($($tt:tt)*)=>{
        pyo3::Python::with_gil(|py| {
            py.eval(
                &format!("print('''{}''')",format!($($tt)*)),
                None,
                None,
            ).unwrap();
        })
    }
}
trait FromCollect<ItemNew>: FromIterator<ItemNew> {
    fn from_collect(x: impl IntoIterator<Item = impl Into<ItemNew>>) -> Self;
}

impl<ItemNew, T: FromIterator<ItemNew>> FromCollect<ItemNew> for T {
    fn from_collect(x: impl IntoIterator<Item = impl Into<ItemNew>>) -> Self {
        x.into_iter().map(Into::into).collect()
    }
}

pub trait IterInto<Item>: IntoIterator<Item = Item> {
    fn into_collect<ItemNew, B: FromIterator<ItemNew>>(self) -> B
    where
        Item: Into<ItemNew>;

    fn into_iter_into<ItemNew>(
        self,
    ) -> std::iter::Map<<Self as IntoIterator>::IntoIter, fn(Item) -> ItemNew>
    where
        Item: Into<ItemNew>;
}

impl<Item, T: IntoIterator<Item = Item>> IterInto<Item> for T {
    fn into_collect<ItemNew, B: FromIterator<ItemNew>>(self) -> B
    where
        Item: Into<ItemNew>,
    {
        self.into_iter_into().collect()
    }

    fn into_iter_into<ItemNew>(
        self,
    ) -> std::iter::Map<<Self as IntoIterator>::IntoIter, fn(Item) -> ItemNew>
    where
        Item: Into<ItemNew>,
    {
        self.into_iter().map(Into::into)
    }
}

pub enum EmptySingleMany<T> {
    Empty,
    Single(T),
    Many(Vec<T>),
}

impl<T> EmptySingleMany<T> {
    pub fn new(mut x: Vec<T>) -> Self {
        if x.is_empty() {
            Self::Empty
        } else if x.len() == 1 {
            Self::Single(x.pop().unwrap().into())
        } else {
            Self::Many(x)
        }
    }
}

impl<T> From<Vec<T>> for EmptySingleMany<T> {
    fn from(x: Vec<T>) -> Self {
        EmptySingleMany::new(x)
    }
}

pub fn split_first_take<T: Default>(x: &mut [T]) -> Option<(T, impl Iterator<Item = T> + '_)> {
    x.split_first_mut()
        .map(|(l, r)| (mem::take(l), r.into_iter().map(mem::take)))
}

pub fn flip_op_result<T, E>(x: Option<Result<T, E>>) -> Result<Option<T>, E> {
    x.map_or(Ok(None), |x| x.map(Some))
}

pub fn as_sorted<Item: Ord>(x: impl IntoIterator<Item = Item>) -> Vec<Item> {
    let mut out: Vec<_> = x.into_iter().collect();
    out.sort();
    out
}

// https://github.com/rust-lang/rust/pull/91589
#[inline]
pub fn arc_ref_clone<T: Clone>(x: &Arc<T>) -> T {
    arc_unwrap_or_clone(x.clone())
}
#[inline]
pub fn arc_unwrap_or_clone<T: Clone>(x: Arc<T>) -> T {
    Arc::try_unwrap(x).unwrap_or_else(|arc| (*arc).clone())
}
#[inline]
pub fn rc_unwrap_or_clone<T: Clone>(x: Rc<T>) -> T {
    Rc::try_unwrap(x).unwrap_or_else(|rc| (*rc).clone())
}

#[macro_export]
macro_rules! simple_from {
    (|$var:ident : $a:ty| -> $b:ty { $($fill:tt)* }) => {
        impl From<$a> for $b {
            fn from($var: $a) -> Self {
                $($fill)*
            }
        }

    };
}

#[macro_export]
macro_rules! simple_default {
    ($a:ty { $($fill:tt)* }) => {
        impl Default for $a {
            fn default() -> Self {
                $($fill)*
            }
        }

    };
}
