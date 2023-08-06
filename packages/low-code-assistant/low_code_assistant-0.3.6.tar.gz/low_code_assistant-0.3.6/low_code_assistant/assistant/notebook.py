from typing import Callable, Dict, Optional

save_notebook: Optional[Callable[[Callable[[bool], None]], None]] = None
markdown_cells: Optional[Dict] = None
