const raw_input = loadFile("/home/anon/aoc-2021/03/input.txt");

const numbers = raw_input.split('\n').filter(s => s != "");
if (numbers.length === 0)
    throw new Exception("Wrong input");
const bit_size = numbers[0].length;
console.log();
console.log(numbers.length, bit_size);

const bit_sums = numbers.map(s => {
    return s.split('').map(b => parseInt(b));
}).reduce((acc, val) => {
    return acc.map((acc_val, i) => acc_val + val[i]);
}, new Array(bit_size).fill(0));

const most_common = bit_sums.map(val => val > numbers.length / 2 ? 1 : 0);
const least_common = most_common.map(v => 1 - v);

function binaryArrayToNumber(arr) {
    const stringValue = arr.reduce((a, b) => a + b, "");
    console.log(stringValue);
    return parseInt(stringValue, 2);
}

console.log(JSON.stringify(most_common));
const gammaRate = binaryArrayToNumber(most_common);
console.log(JSON.stringify(least_common));
const epsilonRate = binaryArrayToNumber(least_common);
// PART 1
console.log(gammaRate, epsilonRate, gammaRate * epsilonRate);

function sum_to_common(val, length=numbers.length) {
    if (val === length / 2) {
        return -1;
    }
    return (val < (length / 2)) ? 0 : 1;
}

const common_counts = bit_sums.map(sum_to_common);

console.log(JSON.stringify(common_counts));

// Does not contain any -1 so I guess this might be lucky?

const bits = numbers.map(s => {
    return s.split('').map(b => parseInt(b));
});

function filterNumbers(input, mostCommon, ifEqual) {
    let nums = input.map(i => i);
    const keep = common_counts.map(v => mostCommon ? v : 1 - v);
    let bit_index = 0;
    while (nums.length > 1 && bit_index < bit_size) {
        const sum_of_bits = nums.map(arr => arr[bit_index])
                                    .reduce((acc, val) => acc + val, 0);
        let common = sum_to_common(sum_of_bits, nums.length);
        console.log('Common ', common);
        if (common == -1)
            common = ifEqual;
        else if (!mostCommon)
            common = 1 - common;

        nums = nums.filter((arr) => arr[bit_index] === common);
        console.log(nums.length, 'left', bit_index);
        bit_index++;
    }
    if (bit_index >= bit_size && nums.length > 1)
        throw "Reached end of bits without single solution";
    return nums[0];
}

const oxygenGen = binaryArrayToNumber(filterNumbers(bits, true, 1));
const co2Scrubbing = binaryArrayToNumber(filterNumbers(bits, false, 0));

console.log(oxygenGen, co2Scrubbing, oxygenGen * co2Scrubbing);





