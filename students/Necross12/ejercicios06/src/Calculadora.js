export class StringCalculator {
    add(numbers) {
        if (numbers === "")
            return 0;

        if (numbers.includes(",")) {
            const parts = numbers.split(",");
            return parseInt(parts[0]) + parseInt(parts[1]);
        }
        return parseInt(numbers);
    }
}
