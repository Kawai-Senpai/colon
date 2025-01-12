# Colon

A ROS2 build tool that handles dependency resolution and package building.

## Installation

```bash
pip install -e .
```

## Usage

From within a ROS2 workspace:
```bash
colon build
```

Or specify workspace path:
```bash
colon build /path/to/workspace
```

Use verbose output:
```bash
colon build -v
```

## Development

1. Create a virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Install in development mode: `pip install -e .`
