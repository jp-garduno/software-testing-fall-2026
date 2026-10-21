export function add(s) {
	if (s === "")
		return 0;

	nums = s.split(',')
	res = nums.reduce((sum, n) => sum += parseInt(n), 0)
	return parseInt(res)
}
