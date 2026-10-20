export class StringCalculator {
    add(numbers) {
        if (numbers === "")
            return 0;

        numbers = numbers.replace(/\n/g, ",");
        const parts = numbers.split(",");
        return parts.reduce((sum, part) => sum + parseInt(part), 0);
    }
}
