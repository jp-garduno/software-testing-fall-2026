import { add } from './calculator.js'

test('return 0 if empty string', () => {
	expect(add("")).toBe(0);
})

test('evaluate single digits', () => {
	expect (add("1")).toBe(1)
	expect (add("5")).toBe(5)
})

test('perform sum of two numbers with comma separation', () => {
	expect (add("1,2")).toBe(3)
	expect (add("5,10")).toBe(15)
})