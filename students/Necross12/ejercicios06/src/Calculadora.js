export class StringCalculator {
    add(numbers) {
        if (numbers === "")
            return 0;

        let delimiter = /[,\n]/;
        let input = numbers;

        if (numbers.startsWith("//")) {
            const [delimiterLine, ...inputLines] = numbers.split("\n");
            const customDelimiter = delimiterLine.slice(2);
            const escapedDelimiter = customDelimiter.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
            delimiter = new RegExp(`${escapedDelimiter}|\n`);
            input = inputLines.join("\n");
        }

        const intParts = input.split(delimiter).map((part) => parseInt(part));
        const negatives = intParts.filter((n) => n < 0);
        if (negatives.length > 0)
            throw new Error(`negatives not allowed: ${negatives.join(", ")}`);

        const validNumbers = intParts.filter((n) => n <= 1000);

        return validNumbers.reduce((sum, n) => sum + n, 0);
    }
}
