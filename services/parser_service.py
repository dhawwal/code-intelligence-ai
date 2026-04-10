from typing import List, Dict
import os
from tree_sitter import Language, Parser
import tree_sitter_python
import tree_sitter_javascript
from utils.file_utils import get_code_files

# Setup Languages
PY_LANGUAGE = Language(tree_sitter_python.language())
JS_LANGUAGE = Language(tree_sitter_javascript.language())
# Note: Further language bindings for Java/TS can be added similarly.
# We map simple extensions to available parsers.
LANGUAGE_MAP = {
    ".py": PY_LANGUAGE,
    ".js": JS_LANGUAGE,
    ".jsx": JS_LANGUAGE,
    ".ts": JS_LANGUAGE, # Fallback TS to JS tree-sitter since bindings are identical structurally for AST basic symbols
    ".tsx": JS_LANGUAGE
}

def parse_repository(repo_path: str) -> List[Dict]:
    """
    Iterates through all supported files in the newly cloned repo and extracts functions/classes.
    """
    files = get_code_files(repo_path)
    all_symbols = []
    
    for file_path in files:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in LANGUAGE_MAP:
            lang = LANGUAGE_MAP[ext]
            symbols = extract_symbols_from_file(file_path, lang, repo_path)
            all_symbols.extend(symbols)
            
    return all_symbols


def extract_symbols_from_file(filepath: str, language: Language, repo_path: str) -> List[Dict]:
    symbols = []
    parser = Parser(language)

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        source_code = f.read()
        
    tree = parser.parse(bytes(source_code, "utf8"))
    root_node = tree.root_node
    
    relative_path = os.path.relpath(filepath, repo_path)

    # Simplified tree walk to extract classes and functions
    # For a full production implementation, specific tree-sitter queries are ideal
    def traverse(node):
        if node.type in ["class_definition", "function_definition", "class_declaration", "function_declaration", "method_definition", "arrow_function"]:
            # Get the name identifier
            name_node = None
            for child in node.children:
                if child.type == "identifier":
                    name_node = child
                    break
            
            name = name_node.text.decode('utf8') if name_node else "anonymous"
            content = source_code[node.start_byte:node.end_byte]
            
            symbols.append({
                "name": name,
                "type": node.type,
                "file": relative_path,
                "line": node.start_point[0] + 1,
                "content": content
            })
            
        for child in node.children:
            traverse(child)

    traverse(root_node)
    
    # If no symbols found (e.g. just scripts or configs), save the whole file as one generic snippet
    if not symbols:
        symbols.append({
            "name": "module_scope",
            "type": "file",
            "file": relative_path,
            "line": 1,
            "content": source_code[:2000] # Cap size for safety
        })

    return symbols
