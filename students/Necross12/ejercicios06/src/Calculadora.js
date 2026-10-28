export class StringCalculator {
    add(numbers) {
        if (numbers === "")
            return 0;

        let delimiters = [","];

        // Parse custom delimiter(s)
        if (numbers.startsWith("//")) {
            const delimiterEnd = numbers.indexOf("\n");
            if (delimiterEnd === -1)
                throw new Error("invalid delimiter format: missing newline after delimiter");
            const delimiterSpec = numbers.substring(2, delimiterEnd);

            // Multiple delimiters in brackets
            const bracketPattern = /\[([^\]]+)\]/g;
            const matches = [...delimiterSpec.matchAll(bracketPattern)];

            if (matches.length > 0)
                delimiters = matches.map((m) => m[1]);
            else
                delimiters = [delimiterSpec];
            numbers = numbers.substring(delimiterEnd + 1);
        }

        // Replace all delimiters with commas
        numbers = numbers.replace(/\n/g, ",");
        delimiters.forEach((delimiter) => {
            const escapedDelimiter = delimiter.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
            numbers = numbers.replace(new RegExp(escapedDelimiter, "g"), ",");
        });

        // Parse numbers
        const parts = numbers.split(",").filter((p) => p !== "");
        const intParts = parts.map((p) => parseInt(p));

        // Check for negatives
        const negatives = intParts.filter((n) => n < 0);
        if (negatives.length > 0)
            throw new Error(`negatives not allowed: ${negatives.join(", ")}`);

        // Ignore numbers > 1000
        const validNumbers = intParts.filter((n) => n <= 1000);
        return validNumbers.reduce((sum, n) => sum + n, 0);
    }
}
