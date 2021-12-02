const std = @import("std");


pub fn part1(file_string: []u8) anyerror!void { 
    var horizontal : i64 = 0;
    var vertical : i64 = 0;

    var lines = std.mem.tokenize(file_string, "\r\n");
    while (lines.next()) |line| {
        if (line.len == 0)
            continue;
        var parts = std.mem.split(line, " ");
        
        const command = parts.next() orelse { return error.InputError; };
        const step_str = parts.next() orelse { return error.InputError; };
        
        const step_size = try std.fmt.parseInt(i32, step_str, 10);
    
//        std.log.info("Read line: {s} with size {d}", .{command, step_size});
        
        if (std.mem.eql(u8, command, "forward")) {
            horizontal += step_size;
        } else if (std.mem.eql(u8, command, "up")) {
            vertical -= step_size;
        } else if (std.mem.eql(u8, command, "down")) {
            vertical += step_size;
        } else {
            return error.InputError;
        }
    }
    
    std.log.info("At the end at depth {d} and hori {d}", .{vertical, horizontal});
    std.log.info("Product {d}", .{vertical * horizontal});
}

pub fn part2(file_string: []u8) anyerror!void {
    var horizontal : i64 = 0;
    var vertical : i64 = 0;
    var aim : i64 = 0;

    var lines = std.mem.tokenize(file_string, "\r\n");
    while (lines.next()) |line| {
        if (line.len == 0)
            continue;
        var parts = std.mem.split(line, " ");
        
        const command = parts.next() orelse { return error.InputError; };
        const step_str = parts.next() orelse { return error.InputError; };
        
        const step_size = try std.fmt.parseInt(i32, step_str, 10);
    
//        std.log.info("Read line: {s} with size {d}", .{command, step_size});
        
        if (std.mem.eql(u8, command, "forward")) {
            horizontal += step_size;
            vertical += aim * step_size;
        } else if (std.mem.eql(u8, command, "up")) {
            aim -= step_size;
        } else if (std.mem.eql(u8, command, "down")) {
            aim += step_size;
        } else {
            return error.InputError;
        }
    }
    
    std.log.info("At the end at depth {d} and hori {d}", .{vertical, horizontal});
    std.log.info("Product {d}", .{vertical * horizontal});
}

pub fn main() anyerror!void {
    var alloc = std.heap.GeneralPurposeAllocator(.{}){};
    defer std.debug.assert(!alloc.deinit());
    var allocator: *std.mem.Allocator = &alloc.allocator;

    var args_it = std.process.args();
    _ = args_it.skip();
    
    const file_name = try (args_it.next(allocator) orelse {
        std.debug.print("Give file name\n", .{});
        return error.InvalidArgs;
    });

    defer allocator.free(file_name);

    var nums = std.ArrayList(u32).init(allocator);
    defer nums.deinit();

    var cwd = std.fs.cwd();
    const file_string : []u8 = try cwd.readFileAlloc(allocator, file_name, std.math.maxInt(usize) );
    defer allocator.free(file_string);
    
    std.log.info("Read file: size {d}", .{file_string.len});

    try part2(file_string);
    
}
