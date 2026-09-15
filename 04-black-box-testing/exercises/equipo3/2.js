describe("Flight Booking Eligibility", () => {
    test("Infant (age 1) with adult - should be free", () => {
        const result = calculatePrice({
            age: 1,
            ticketClass: "Economy",
            withAdult: true,
            bags: 0,
        });
        expect(result.price).toBe(0);
        expect(result.requiresAdult).toBe(true);
    });

    test("Child (age 8) - 50% discount", () => {
        const result = calculatePrice({
            age: 8,
            ticketClass: "Economy",
            basePrice: 200,
        });
        expect(result.price).toBe(100);
    });

    test("Teen (age 15) with adult - 10% discount", () => {
        const result = calculatePrice({
            age: 15,
            ticketClass: "Economy",
            withAdult: true,
            basePrice: 200,
        });
        expect(result.price).toBe(180);
    });

    // TODO: Complete all age categories
});