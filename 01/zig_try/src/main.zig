const std = @import("std");

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
    
    //std.log.info("Read file: _{s}_", .{file_string});

    var lines = std.mem.tokenize(file_string, "\r\n");
    while (lines.next()) |line| {
        const num = try std.fmt.parseInt(u32, line, 10);
        try nums.append(num);
    }
    const len = nums.items.len;

    if (len == 0) {
        std.log.info("No entries?", .{});
        return;
    }

    std.log.info("Read {d} lines, first {d}", .{len, nums.items[0]});
    
    
    var last = nums.items[0];
    var increasing: u32 = 0;
    
    for (nums.items) |val, index| {
        if (index == 0)
            continue;

        if (val > last)
            increasing += 1;
        last = val;
    }
    
    
    if (len < 3) {
        std.log.info("Not enough entries", .{});
        return;
    }
    
    
    std.log.info("Found {d} increasing pairs", .{increasing});
}
