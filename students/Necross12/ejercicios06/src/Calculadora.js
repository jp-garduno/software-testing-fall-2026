export class StringCalculator {
    add(numbers) {
        if (numbers === "")
            return 0;

        let delimiter = /[,\n]/;
        let input = numbers;

        if (numbers.startsWith("//")) {
            const delimiterEnd = numbers.indexOf("\n");
            const delimiterSpec = numbers.substring(2, delimiterEnd);

            if (delimiterSpec.startsWith("[") && delimiterSpec.endsWith("]"))
                delimiter = delimiterSpec.slice(1, -1);
            else
                delimiter = delimiterSpec;
            input = numbers.substring(delimiterEnd + 1);
        }

        const intParts = input.split(delimiter).map((part) => parseInt(part));
        const negatives = intParts.filter((n) => n < 0);
        if (negatives.length > 0)
            throw new Error(`negatives not allowed: ${negatives.join(", ")}`);

        const validNumbers = intParts.filter((n) => n <= 1000);

        return validNumbers.reduce((sum, n) => sum + n, 0);
    }
}
