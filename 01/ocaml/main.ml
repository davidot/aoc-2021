let read_file filename =
    let channel = open_in filename in
    let s = really_input_string channel (in_channel_length channel) in
    close_in channel;
    s

let read_nums input_text =
    input_text
    |> String.trim
    |> String.split_on_char '\n'
    |> List.map String.trim
(*    |> List.filter (fun s -> String.length s > 0)*)
    |> List.map int_of_string
    


let rec count_inc' s l =
    match l with
        a :: b :: tail -> let s' = s + (if b > a then 1 else 0) in
                                count_inc' s' (b :: tail)
        | _ -> s
    
let count_inc l =
    count_inc' 0 l

let part1 nums =
    nums
    |> count_inc


let rec calc_windows l =
    match l with
        a :: b :: c :: tail -> (a + b + c) :: calc_windows (b :: c :: tail)
        | _ -> []

let yikes x =
    print_endline (x |> List.length |> Int.to_string);
    x

let part2 nums =
    nums
    |> calc_windows
(*    |> yikes *)
    |> count_inc


let solve input_text = 
    let nums = input_text |> read_nums in
    print_endline "Part 1: ";
    print_endline (nums |> part1 |> Int.to_string);
    print_endline "Part 2: ";
    print_endline (nums |> part2 |> Int.to_string)
    
    

let () = 
    Sys.argv.(1)
    |> read_file
    |> solve

