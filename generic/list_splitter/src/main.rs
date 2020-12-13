use std::fs::OpenOptions;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::env;
use std::process;
use std::io::Write;
use std::iter::Iterator;


fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 3 {
        println!("Usage:");
        println!("list_splitter <filepath> <splitsize>");
        process::exit(1);
    }

    let filepath = &args[1];
    let splitter = &args[2];
    let splitter: usize = match splitter.trim().parse() {
        Ok(num) => num,
        Err(_) => {
            println!("Couldn't convert splitter to integer");
            process::exit(1);
        },
    };

    let mut lines_vec: Vec<String> = Vec::new();
    // File hosts must exist in current path before this produces output
    if let Ok(lines) = read_lines(&filepath) {
        // Consumes the iterator, returns an (Optional) String
        for line in lines {
            if let Ok(l) = line {
                lines_vec.push(l);
            }
        }

        let split_size = lines_vec.len() / splitter;
        let mut v_slices: Vec<Vec<String>> = lines_vec.chunks(split_size).map(|x| x.to_vec()).collect();

        if v_slices.len() > splitter {
            let remainder = v_slices.pop();
            let mut loopvar = 0;
            for array in remainder {
                for element in array {
                    v_slices[loopvar].push(element);
                    loopvar = loopvar + 1;
                }
            }
        }

        let mut file_suffix = splitter;
        for n in 0..splitter {
            let file_to_write = filepath.to_string() + "_split" + &file_suffix.to_string();
            let mut file = OpenOptions::new()
                    .create(true)
                    .write(true)
                    .append(true)
                    .open(&file_to_write)
                    .unwrap();
            for element in v_slices[n].iter() {
                
                if let Err(e) = writeln!(file, "{}", element) {
                    eprintln!("Couldn't write to file: {}", e);
                }
            }
            file_suffix = file_suffix - 1;
        }
    }
}
// The output is wrapped in a Result to allow matching on errors
// Returns an Iterator to the Reader of the lines of the file.
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}