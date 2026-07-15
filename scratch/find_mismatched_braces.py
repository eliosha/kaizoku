with open("/Users/mac/Desktop/Websites /GITkaizoku/main.js") as f:
    content = f.read()

stack = []
line_no = 1
col_no = 1

# Ignore inside strings and comments
in_single_quote = False
in_double_quote = False
in_template_literal = False
in_regex = False
in_line_comment = False
in_block_comment = False

escaped = False

for idx, char in enumerate(content):
    if char == '\n':
        line_no += 1
        col_no = 1
    else:
        col_no += 1
        
    if escaped:
        escaped = False
        continue
        
    if char == '\\':
        escaped = True
        continue
        
    if in_line_comment:
        if char == '\n':
            in_line_comment = False
        continue
        
    if in_block_comment:
        if char == '/' and content[idx-1] == '*':
            in_block_comment = False
        continue
        
    if in_single_quote:
        if char == "'":
            in_single_quote = False
        continue
        
    if in_double_quote:
        if char == '"':
            in_double_quote = False
        continue
        
    if in_template_literal:
        if char == '`':
            in_template_literal = False
        continue
        
    # Check for comments
    if char == '/' and idx + 1 < len(content):
        if content[idx+1] == '/':
            in_line_comment = True
            continue
        elif content[idx+1] == '*':
            in_block_comment = True
            continue
            
    # Check for strings
    if char == "'":
        in_single_quote = True
        continue
    if char == '"':
        in_double_quote = True
        continue
    if char == '`':
        in_template_literal = True
        continue
        
    # Track brackets
    if char in ('{', '(', '['):
        stack.append((char, line_no, col_no))
    elif char in ('}', ')', ']'):
        if not stack:
            print(f"Extra closing character '{char}' at line {line_no}, col {col_no}")
        else:
            top_char, top_line, top_col = stack.pop()
            # Check match
            matches = {'}': '{', ')': '(', ']': '['}
            if matches[char] != top_char:
                print(f"Mismatch: '{char}' at line {line_no}, col {col_no} closes '{top_char}' from line {top_line}, col {top_col}")

print(f"Finished scanning. Stack size: {len(stack)}")
if stack:
    print("Unclosed brackets in stack (top 10):")
    for b, l, c in stack[-10:]:
        print(f"  '{b}' opened at line {l}, col {c}")
