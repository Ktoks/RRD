use clap::{App, Arg};
use regex::Regex;
use std::fs::File;
use std::io::{prelude::*, BufReader, BufWriter};

fn main() {
    ////////////////////////////////// Declare variables //////////////////////////////////
    // get command line arguments
    let matches = cli();

    // get the files
    let out_path = matches.value_of("output").unwrap(); // unwrap OK because required arg
    let in_path = matches.value_of("input").unwrap(); // unwrap OK because required arg

    // bufreading
    let f = File::open(in_path).expect("Unable to open file");
    let f = BufReader::new(f);

    // xml string to be written out
    let mut xml_out: String = String::new();

    // string starts with anything but a '<'    ([^<\s]+\s*)+<   (\S+\s*)+<
    let special_perc = Regex::new(r#"(\S+\s*)+<"#).unwrap();
    // let special_perc = Regex::new(r"(\s*[^<\s]+\s*)+<").unwrap();
    // let get_special = Regex::new(r"(%%)").unwrap();

    // perl
    let begin_cdata = Regex::new(r#"<!\[CDATA\["#).unwrap(); // CDATA in line
    let end_cdata = Regex::new(r#"]]"#).unwrap(); // End in line
    let semicolon = Regex::new(r#";"#).unwrap();
    let curly = Regex::new(r#"[{}]"#).unwrap();
    let curly_semi = Regex::new(r#"[{;}]"#).unwrap();
    let cdata_comment = Regex::new(r#"\s+#"#).unwrap();
    let just_cdata_comment_loc = Regex::new(r#"#[^\n]+\n"#).unwrap();
    let is_comment = Regex::new(r#"#[^;{}]+[;{}]"#).unwrap();

    let mut perl_code: String = String::new();
    let mut in_cdata = false;

    // looking for whitespace in body of text
    let rm_ws = Regex::new(r"\s+").unwrap();

    // comments
    let xml_comment_body = Regex::new(r#"<!--.*[^-][^-]"#).unwrap();

    // handle ? xml line
    let xml_file_version = Regex::new(r#"<\?[^?]*\?"#).unwrap();

    // head xml lines
    let head_string = Regex::new(r#"<(\w+)"#).unwrap(); // <powerstream

    // handle body lines
    let bod_strings = Regex::new(r#"(\s*[[:word:]]+="[^"/]*")+"#).unwrap(); //  win_run_path="%%runpath2" unix_run_path="%%runpath" name="powerstream"
    let in_declaration = Regex::new(r#"^\s*(.+)=$"#).unwrap(); // memo=
    let in_quotes = Regex::new(r#"[^=]$"#).unwrap(); // "string to be saved"
    let end_slash = Regex::new(r#"\s+/"#).unwrap(); // "/>"

    // handle foot lines
    let foot_slash = Regex::new(r#"</[[:word:]]+"#).unwrap(); // </powerstream

    // count tabs
    let mut tab_mult: usize = 0;

    ////////////////////////////////// End Declare variables //////////////////////////////////

    // loop over the file
    for n_line in f.split(b'>') {
        // line cleanup
        let line = n_line.expect("Unable to read line");
        let line = std::str::from_utf8(&line).unwrap();
        let line = line.replace("\t", "");

        let mut perl_comments: Vec<String> = Vec::new();
        let mut comment_count: usize = 0;

        // handle perl comment issue before line breaks
        if cdata_comment.is_match(&line) {
            for comment in just_cdata_comment_loc.find_iter(&line) {
                perl_comments.push(line[comment.start()..comment.end()].to_string());
            }
            // println!("comments: {}",perl_comments);
        }

        let line = line.replace("\n", " ");
        let line = line.replace("  ", " ");
        let line = line.replace("  ", " ");

        // handle perl lines
        if begin_cdata.is_match(&line) || in_cdata {
            in_cdata = true;

            if line.is_empty() {
                perl_code = [perl_code, '>'.to_string()].concat();
                continue;
            }

            perl_code = [perl_code, line[..].to_string()].concat();

            // if '>' in perl code, add one and continue
            if !end_cdata.is_match(&line) {
                perl_code = [perl_code, '>'.to_string()].concat();
                continue;
            }

            // find loc of <[CDATA[]]>
            let cdata_loc = begin_cdata.find(&perl_code).unwrap();
            let end_perl_loc = end_cdata.find(&perl_code).unwrap();

            // get <[CDATA[*]]> just the star
            perl_code = perl_code[cdata_loc.end()..end_perl_loc.start()].to_string();

            let mut temp_perl = String::new();

            // check for ;
            if semicolon.is_match(&perl_code) {
                let mut last_cs: usize = 0;
                // add newline after cdata
                temp_perl = [
                    temp_perl,
                    '\n'.to_string(),
                    // "\t".to_string().repeat(tab_mult),
                ]
                .concat();

                // check for comments
                if is_comment.is_match(&perl_code) {
                    for temp_comment_loc in is_comment.find_iter(&perl_code) {
                        // match this comment with comments found earlier
                        let perl_code_clone = &perl_code.clone();
                        let cloned_chunk =
                            &perl_code_clone[temp_comment_loc.start()..temp_comment_loc.end() + 1];
                        // if they match each other
                        if &cloned_chunk[0..perl_comments[comment_count].len() - 1] == &perl_comments[comment_count][..perl_comments[comment_count].len() - 1] {
                            temp_perl = [
                                '\t'.to_string().repeat(tab_mult),
                                perl_code[..temp_comment_loc.start()].to_string(),
                                '\n'.to_string(),
                                '\t'.to_string().repeat(tab_mult),
                                perl_comments[comment_count].to_string(),
                            ]
                            .concat();
                            comment_count += 1;
                        }
                    }
                }

                // check for {}
                if curly.is_match(&perl_code) {
                    for current_cs in curly_semi.find_iter(&perl_code) {
                        // add before tab
                        temp_perl = [temp_perl, '\t'.to_string().repeat(tab_mult)].concat();
                        
                        // if it's an open curly
                        if &perl_code[current_cs.start()..current_cs.start() + 1] == "{" {
                            temp_perl = [
                                temp_perl,
                                perl_code[last_cs..current_cs.end() - 1].to_string(),
                                "\n".to_string(),
                                "\t".to_string().repeat(tab_mult),
                                "{\n".to_string(),
                            ]
                            .concat();
                            last_cs = current_cs.end();
                            tab_mult += 1;
                        }

                        // if it's a semi-colon
                        else if &perl_code[current_cs.start()..current_cs.start() + 1] == ";" {
                            temp_perl = [
                                temp_perl,
                                perl_code[last_cs..current_cs.end()].to_string(),
                                "\n".to_string(),
                            ]
                            .concat();
                            last_cs = current_cs.end();
                        }
                        // if it's a close curly
                        else if &perl_code[current_cs.start()..current_cs.start() + 1] == "}" {
                            temp_perl = [
                                temp_perl,
                                perl_code[last_cs..current_cs.end()].to_string(),
                                "\n".to_string(),
                            ]
                            .concat();
                            tab_mult -= 1;
                        }
                    }
                    temp_perl = [temp_perl, "\t".to_string().repeat(tab_mult)].concat();
                } else {
                    for prl in perl_code.split(';') {
                        temp_perl = [
                            temp_perl,
                            // "\n".to_string(),
                            "\t".to_string().repeat(tab_mult),
                            prl.to_string(),
                            ";\n".to_string(),
                        ]
                        .concat();
                    }
                    // get rid of extra ';'
                    temp_perl.pop();
                    temp_perl.pop();
                }
                // temp_perl = [temp_perl, "\t".to_string().repeat(tab_mult)].concat();
                perl_code = temp_perl;
            }
            // let mut temp = String::new();
            // found perl, split on ';'
            // if semicolon.is_match(&perl_code) {
            //     for prl in perl_code.split(';') {
            //         temp = [
            //             temp,
            //             "\n".to_string(),
            //             "\t".to_string().repeat(tab_mult),
            //             prl.to_string(),
            //             ';'.to_string(),
            //         ]
            //         .concat();
            //     }
            //     // get rid of extra ';'
            //     temp.pop();
            //     // temp = [temp, "\n".to_string(), "\t".to_string().repeat(tab_mult)].concat();
            // }

            // temp = [temp, perl_code.to_string()].concat();

            // send cdata end to xml_out
            xml_out = [
                xml_out,
                "\t".to_string().repeat(tab_mult),
                "<![CDATA[".to_string(),
                perl_code,
                "]]>\n".to_string(),
            ]
            .concat();

            perl_code = String::new();
            in_cdata = false;
            continue;
        }

        // todo: I need to fix this- it's not handling the outside elements correctly. Also need to do better perl formatting
        // handle outside of elements
        if special_perc.is_match(&line) {
            let spec = special_perc.find(&line).unwrap();
            xml_out = [
                xml_out,
                // "\n".to_string(),
                "\t".to_string().repeat(tab_mult),
                line[spec.start()..spec.end() - 1].to_string(),
                "\n".to_string(),
            ]
            .concat();
            // continue;
        }

        // handle xml comments
        if xml_comment_body.is_match(&line) {
            let c_bod = xml_comment_body.find(&line).unwrap();
            // println!("{}", &line);
            xml_out = [
                xml_out,
                "\t".to_string().repeat(tab_mult),
                line[c_bod.start()..c_bod.end()].to_string(),
                "-->\n".to_string(),
            ]
            .concat();
            continue;
        }

        // handle the ? header
        if xml_file_version.is_match(&line) {
            xml_out = [xml_out, line[..].to_string(), ">\n".to_string()].concat();
            continue;
        }

        // handle normal xml
        let mut xml_peices = String::new();

        // handle header
        if head_string.is_match(&line) {
            // get the header
            let head = head_string.find(&line).unwrap();
            xml_peices = [
                xml_peices,
                "\t".to_string().repeat(tab_mult),
                line[head.start()..head.end()].to_string(),
                "\n".to_string(),
            ]
            .concat();
            tab_mult += 1;
        }

        // handle body of xml
        if bod_strings.is_match(&line) {
            let bod = bod_strings.find(&line).unwrap();

            let peices = line[bod.start()..bod.end()].to_string();
            let mut to_concat = String::new();
            let mut dec = false;

            // for loop to stack each body peice
            for peice in peices.split('"') {
                if in_declaration.is_match(peice) {
                    dec = true;
                    let temp = peice.replace(" ", "");
                    to_concat = [
                        to_concat,
                        "\t".to_string().repeat(tab_mult),
                        temp.to_string(),
                    ]
                    .concat();
                } else if in_quotes.is_match(peice) {
                    let temp = rm_ws.replace_all(peice, " ");
                    let temp = temp.to_string();

                    to_concat = [
                        to_concat,
                        '"'.to_string(),
                        temp.to_string(),
                        '"'.to_string(),
                        '\n'.to_string(),
                    ]
                    .concat();
                    dec = false;
                } else if peice.is_empty() && dec {
                    to_concat = [to_concat, "\"\"".to_string(), '\n'.to_string()].concat();
                } else {
                    to_concat.pop();
                }
            }
            xml_peices = [xml_peices, to_concat.to_string(), "\n".to_string()].concat();
        }

        // handle "/>" (self closing / no children)
        if end_slash.is_match(&line) {
            tab_mult -= 1;
            xml_peices = [
                xml_peices,
                "\t".to_string().repeat(tab_mult),
                "/>\n".to_string(),
            ]
            .concat();
        }
        // handle </powerstream (footer / end of children and self)
        else if foot_slash.is_match(&line) {
            let foot = foot_slash.find(&line).unwrap(); // have to find, this could be on the same line as other <>'s
            xml_peices = [
                xml_peices,
                "\t".to_string().repeat(tab_mult - 1),
                line[foot.start()..foot.end()].to_string(),
                ">\n".to_string(),
            ]
            .concat();
            tab_mult -= 1;
        } else {
            if !xml_peices.is_empty() {
                xml_peices = [
                    xml_peices,
                    "\t".to_string().repeat(tab_mult),
                    ">\n".to_string(),
                ]
                .concat();
            }
        }

        xml_out = [xml_out, xml_peices.to_string()].concat();
    }

    // writing
    let out_f = File::create(out_path).expect("Couldn't create file!");
    let mut out_f = BufWriter::new(out_f);
    out_f
        .write_all(xml_out.as_bytes())
        .expect("Couldn't write contents out!");
}

// command line
fn cli() -> clap::ArgMatches<'static> {
    let matches = App::new("XML fmt")
        .args(&[
            Arg::with_name("input")
                .required(true)
                .index(1)
                .help("the input file to use"),
            Arg::with_name("output")
                .short("o")
                .required(true)
                .takes_value(true)
                .help("the output file to use"),
        ])
        .get_matches();
    matches
}
