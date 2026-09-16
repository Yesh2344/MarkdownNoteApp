# MarkdownNoteApp

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-lightgrey.svg)](https://palletsprojects.com/p/flask/)

## Overview

MarkdownNoteApp is a lightweight, production‑ready web application that lets users write, preview, and persist Markdown notes. The front‑end is built with modern HTML5, CSS3, and vanilla JavaScript (using the **marked** library for rendering). The back‑end is a Flask API that safely stores notes on disk, with proper configuration handling, logging, and error management.

## Features

- Real‑time Markdown preview
- Save notes to the server via a RESTful API
- Environment‑based configuration (`.env`)
- Comprehensive error handling and logging
- Unit tests with **pytest**
- Fully typed Python code (type hints)

## Quick Start

### Prerequisites

- Python 3.9 or newer
- `git` (optional, for cloning)

### Installation