FROM gitpod/workspace-full-vnc
RUN pip install pytest-playwright
RUN playwright install-deps
RUN playwright install
RUN pip install pytest-playwright-visual