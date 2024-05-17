# 2048 AI

Works with the following web pages:

- [https://play2048.co/](https://play2048.co/)
- [https://ristsona.postimees.ee/2048](https://ristsona.postimees.ee/2048)
- [https://2048game.com/](https://2048game.com/)
- [https://www.2048.org/](https://www.2048.org/)

## Usage:

1. **Create a virtual environment:**

   ```sh
   cd 2048AI
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install all requirements:**

   ```sh
   pip install -r requirements.txt
   ```

3. **Set screen resolution in `config.py` to your screen's resolution:**

   Change these values:

   ```python
   # Screen settings
   screen_width = 1440
   screen_height = 900
   ```

4. **Run `2048ai.py`:**

   ```sh
   python3 2048ai.py
   ```

5. **Make sure to allow all required permissions during the first run in order to enable game controls and screen capture.**

6. **Open one of the web pages listed above.**

7. **Enjoy. The AI is playing for you.**
