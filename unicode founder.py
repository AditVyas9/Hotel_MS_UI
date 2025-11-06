def unicode_escape_form(s: str):
	for ch in s:
		code = ord(ch)
		if code <= 0xFFFF:
			print(f"{ch} → \\u{code:04X}")
		else:
			print(f"{ch} → \\U{code:08X}")