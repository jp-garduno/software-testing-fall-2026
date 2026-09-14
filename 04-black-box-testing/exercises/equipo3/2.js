describe("Flight Booking Eligibility - Equivalence Partitioning Tests", () => {
    const BASE_PRICE = 200;

    // --- AGE TESTS ---
    describe("Age Partitions", () => {
        test("A1: Negative age (-1) - should throw Error", () => {
            expect(() => calculatePrice({ age: -1, ticketClass: "Economy", basePrice: BASE_PRICE })).toThrow("Invalid age");
        });

        test("A2: Infant (age 0) with adult - Free", () => {
            const result = calculatePrice({ age: 0, ticketClass: "Economy", withAdult: true, basePrice: BASE_PRICE });
            expect(result.price).toBe(0);
            expect(result.requiresAdult).toBe(true);
        });

        test("A3: Infant (age 1) with adult - Free", () => {
            const result = calculatePrice({ age: 1, ticketClass: "Economy", withAdult: true, basePrice: BASE_PRICE });
            expect(result.price).toBe(0);
        });

        test("A4: Child lower bound (age 2) - 50% discount", () => {
            const result = calculatePrice({ age: 2, ticketClass: "Economy", basePrice: BASE_PRICE });
            expect(result.price).toBe(100);
        });

        test("A5: Child upper bound (age 11) - 50% discount", () => {
            const result = calculatePrice({ age: 11, ticketClass: "Economy", basePrice: BASE_PRICE });
            expect(result.price).toBe(100);
        });

        test("A6: Teen lower bound (age 12) with adult - 10% discount", () => {
            const result = calculatePrice({ age: 12, ticketClass: "Economy", withAdult: true, basePrice: BASE_PRICE });
            expect(result.price).toBe(180);
        });

        test("A7: Teen upper bound (age 17) with adult - 10% discount", () => {
            const result = calculatePrice({ age: 17, ticketClass: "Economy", withAdult: true, basePrice: BASE_PRICE });
            expect(result.price).toBe(180);
        });

        test("A8: Adult lower bound (age 18) - 0% discount", () => {
            const result = calculatePrice({ age: 18, ticketClass: "Economy", basePrice: BASE_PRICE });
            expect(result.price).toBe(200);
        });

        test("A9: Adult upper bound (age 64) - 0% discount", () => {
            const result = calculatePrice({ age: 64, ticketClass: "Economy", basePrice: BASE_PRICE });
            expect(result.price).toBe(200);
        });

        test("A10: Senior (age 65) - 15% discount", () => {
            const result = calculatePrice({ age: 65, ticketClass: "Economy", basePrice: BASE_PRICE });
            expect(result.price).toBe(170);
        });

        test("A11: Age over maximum bound (age 121) - should throw Error", () => {
            expect(() => calculatePrice({ age: 121, ticketClass: "Economy", basePrice: BASE_PRICE })).toThrow("Invalid age");
        });
    });

    // --- TICKET CLASS & BAGGAGE TESTS ---
    describe("Ticket Class & Baggage Allowance", () => {
        test("B1 & C3: Economy with 2 bags ($30 per bag)", () => {
            const result = calculatePrice({ age: 30, ticketClass: "Economy", bags: 2, frequentFlyer: "None", basePrice: BASE_PRICE });
            expect(result.baggageFee).toBe(60);
        });

        test("B2: Business class - 1 free bag", () => {
            const result = calculatePrice({ age: 30, ticketClass: "Business", bags: 1, frequentFlyer: "None", basePrice: BASE_PRICE });
            expect(result.baggageFee).toBe(0);
        });

        test("B3: First class - 2 free bags", () => {
            const result = calculatePrice({ age: 30, ticketClass: "First", bags: 2, frequentFlyer: "None", basePrice: BASE_PRICE });
            expect(result.baggageFee).toBe(0);
        });

        test("B4: Unknown Class - should throw Error", () => {
            expect(() => calculatePrice({ age: 30, ticketClass: "VIP", basePrice: BASE_PRICE })).toThrow("Invalid class");
        });

        test("C1: Negative bags (-1) - should throw Error", () => {
            expect(() => calculatePrice({ age: 30, ticketClass: "Economy", bags: -1, basePrice: BASE_PRICE })).toThrow("Invalid baggage count");
        });

        test("C4: Bags exceeding max limit (> 2) - should throw Error", () => {
            expect(() => calculatePrice({ age: 30, ticketClass: "Economy", bags: 3, basePrice: BASE_PRICE })).toThrow("Exceeds baggage limit");
        });
    });

    // --- FREQUENT FLYER TESTS ---
    describe("Frequent Flyer Status Partitions", () => {
        test("D3: Economy + Gold status (1 free bag bonus)", () => {
            const result = calculatePrice({ age: 30, ticketClass: "Economy", bags: 1, frequentFlyer: "Gold", basePrice: BASE_PRICE });
            expect(result.baggageFee).toBe(0);
        });

        test("D4: Business + Platinum status (1 free class + 1 free status = 2 free bags)", () => {
            const result = calculatePrice({ age: 30, ticketClass: "Business", bags: 2, frequentFlyer: "Platinum", basePrice: BASE_PRICE });
            expect(result.baggageFee).toBe(0);
        });

        test("D5: Invalid Frequent Flyer Status - should throw Error", () => {
            expect(() => calculatePrice({ age: 30, ticketClass: "Economy", frequentFlyer: "Diamond", basePrice: BASE_PRICE })).toThrow("Invalid status");
        });
    });
});
