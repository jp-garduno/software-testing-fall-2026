export class StringCalculator {
    add(numbers) {
        if (numbers === "")
            return 0;

        let delimiter = ",";

        // Check for custom delimiter
        if (numbers.startsWith("//")) {
            const delimiterEnd = numbers.indexOf("\n");
            delimiter = numbers.substring(2, delimiterEnd);
            numbers = numbers.substring(delimiterEnd + 1);
        }

        // Replace newlines and custom delimiter
        numbers = numbers.replace(/\n/g, ",");
        if (delimiter !== ",") {
            const delimiterRegex = new RegExp(
                delimiter.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"),
                "g"
            );
            numbers = numbers.replace(delimiterRegex, ",");
        }

        const parts = numbers.split(",");
        return parts.reduce((sum, part) => sum + parseInt(part), 0);
    }
}
