"""
Image helper for Calla.

The pages reference images by relative path (e.g. "static/images/stork.png").
This helper:
    - if the file exists on disk → renders it via st.image()
    - if not → shows a labeled placeholder so the page still loads cleanly
              and you can see exactly what filename to put where.

This means you can drop an image into static/images/ and Streamlit's auto-
reload will pick it up without you editing any Python.
"""

import os
import streamlit as st


def render_image_or_placeholder(
    path: str,
    *,
    caption: str | None = None,
    description: str = "",
    **kwargs,
) -> None:
    """
    Show an image at `path` if it exists; otherwise show a placeholder.

    Args:
        path: relative path to the image file (e.g. "static/images/stork.png")
        caption: optional caption shown below the image
        description: short label to show in the placeholder so you know what
                     image is supposed to go there (e.g. "stork flying")
        **kwargs: forwarded to st.image (width, use_container_width, etc.)

    Examples:
        render_image_or_placeholder(
            "static/images/stork.png",
            description="stork flying above",
            width=200,
        )
        render_image_or_placeholder(
            "static/images/mir_castle.jpg",
            caption="Замак у Міры (Mir Castle)",
            description="Mir Castle scene with sky",
            use_container_width=True,
        )
    """
    if os.path.exists(path):
        st.image(path, **kwargs)
        if caption:
            st.caption(caption)
    else:
        # Placeholder — so the page renders even before the image is added.
        # The user can see the expected file path to know what to drop in.
        label = description or "image"
        st.info(
            f"📷 _Drop an image of **{label}** at_ `{path}` _to display it here._"
        )
