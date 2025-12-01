# License

## MIT License

Copyright (c) 2024 Poker Advisor Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Third-Party Licenses and Attributions

This project depends on the following open-source libraries:

### FastAPI
- **License**: MIT
- **Copyright**: (c) Sebastián Ramírez
- **URL**: https://github.com/tiangolo/fastapi
- **Description**: Modern, fast web framework for building APIs with Python

### Uvicorn
- **License**: BSD-3-Clause
- **Copyright**: (c) Tom Christie
- **URL**: https://github.com/encode/uvicorn
- **Description**: Lightning-fast ASGI server implementation

### Pydantic
- **License**: MIT
- **Copyright**: (c) Samuel Colvin
- **URL**: https://github.com/pydantic/pydantic
- **Description**: Data validation and parsing using Python type annotations

### eval7
- **License**: MIT
- **URL**: https://pypi.org/project/eval7/
- **Description**: Fast and accurate poker hand evaluator using 64-bit representations

### Microsoft Azure SDK for Python
- **License**: Apache-2.0
- **URL**: https://github.com/Azure/azure-sdk-for-python
- **Description**: Azure cloud platform SDK for Python (optional, for cloud deployment)

### Starlette
- **License**: BSD-3-Clause
- **URL**: https://github.com/encode/starlette
- **Description**: Lightweight ASGI framework included as FastAPI dependency

---

## Data Attributions

### Poker Hand Ranges
- **Source**: Custom JSON files stored in `/data/ranges/*.json`
- **Format**: JSON
- **Size**: 5-10 KB each
- **License**: Self-developed for this project
- **Notes**: Hand range specifications are based on live poker strategy principles and represent positions in 6-max and full-ring games with 100 big blind stack depth.

### Poker Strategy Resources (Educational Reference)
The following resources informed the strategy implementation:
- Poker Hands Ranked & Free Cheat Sheet Download (WSOP)
- Top Poker Preflop Charts for GTO Strategy (Pokerati)
- Additional poker theory references in `/gametheoryexamples/`

---

## Code Contributions

If you contribute code to this project, you agree that your contributions will be licensed under the same MIT License.

---

## Disclaimer

This project is provided for educational purposes. While efforts have been made to ensure accuracy of poker equity calculations and recommendations, users should independently verify results and exercise their own judgment when making poker decisions. The authors are not responsible for any losses incurred through use of this software.

---

## How to Use These Licenses

1. **For Users**: Simply follow the terms of the MIT License - you can use, modify, and distribute the software freely while including the license text.

2. **For Contributors**: When submitting contributions, ensure that:
   - You have the right to contribute the code
   - Your code complies with the MIT License
   - You provide proper attribution for any third-party code
   - Your changes do not introduce incompatible licenses

3. **For Deployment**: When deploying this software, ensure that all dependencies' licenses are respected (MIT and BSD licenses are generally compatible for redistribution).

---

## Contact

For licensing questions, please open an issue on the project repository.

**Last Updated**: December 2024
