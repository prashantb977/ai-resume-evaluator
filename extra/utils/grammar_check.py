import language_tool_python

def grammar_feedback(text):
    try:
        tool = language_tool_python.LanguageTool('en-US')
        matches = tool.check(text)
        issues = [(m.message, text[m.offset:m.offset + m.errorLength]) for m in matches[:5]]
        return len(matches), issues
    except:
        return 0, []
