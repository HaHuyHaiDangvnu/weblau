"""Streamlit web app for the 12-question crossword game."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from quiz_data import ANSWER, QUESTIONS, validate_puzzle

APP_BACKGROUND = "#245b98"
BUTTON_BACKGROUND = "#006bb3"
WRONG_BACKGROUND = "#dc2626"
CORRECT_BACKGROUND = "#16a34a"
COMPLETION_IMAGE = Path(__file__).resolve().parent / "assets" / "chuc_mung_20_10.png"


def initialize_state() -> None:
    defaults = {
        "revealed": set(),
        "active_cell": None,
        "selected_choice": None,
        "answer_state": None,
        "feedback": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_styles(completed: bool = False) -> None:
    css = [
        f"""
        <style>
        .stApp, [data-testid="stAppViewContainer"] {{
            background: linear-gradient(135deg, #176ba9 0%, {APP_BACKGROUND} 100%) !important;
            color: #172b4d !important;
        }}
        header[data-testid="stHeader"] {{
            display: none !important;
        }}
        .block-container {{
            max-width: 1100px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}
        .game-title {{
            color: #ffffff !important;
            text-align: center;
            font-size: clamp(1.6rem, 4vw, 2.6rem);
            font-weight: 800;
            margin: 0;
        }}
        .game-subtitle {{
            color: #eff6ff !important;
            text-align: center;
            margin: .5rem 0 1.5rem;
        }}
        .st-key-game-panel {{
            background: #ffffff !important;
            color: #172b4d !important;
            border: 2px solid #7dd3fc !important;
            border-radius: 14px !important;
            padding: 1.25rem !important;
        }}
        .st-key-game-panel h1,
        .st-key-game-panel h2,
        .st-key-game-panel h3,
        .st-key-game-panel p,
        .st-key-game-panel label,
        .st-key-game-panel [data-testid="stMarkdownContainer"] {{
            color: #172b4d !important;
        }}
        .st-key-game-panel [data-testid="stAlert"] p {{
            color: inherit !important;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: #ffffff !important;
            border-color: #7dd3fc !important;
            border-radius: 14px !important;
        }}
        div[data-testid="stMetric"] label,
        div[data-testid="stMarkdownContainer"] p {{
            text-align: center;
        }}
        div.st-key-reset-game button,
        div.st-key-reset-game button p {{
            background: {BUTTON_BACKGROUND} !important;
            color: #ffffff !important;
        }}
        """
    ]
    if completed:
        css.append(
            """
            .block-container {
                max-width: none !important;
                padding: 0 !important;
            }
            .st-key-completion-screen {
                width: 100%;
                padding: 0 !important;
                margin: 0 !important;
            }
            .st-key-completion-screen [data-testid="stImage"],
            .st-key-completion-screen [data-testid="stImageContainer"] {
                display: block !important;
                width: 100% !important;
                max-width: none !important;
            }
            .st-key-completion-screen [data-testid="stFullScreenFrame"] > div {
                width: 100% !important;
                max-width: none !important;
            }
            .st-key-completion-screen img {
                width: 100% !important;
                max-height: 100vh;
                object-fit: contain;
            }
            .st-key-completion-screen div.st-key-reset-game {
                display: flex;
                justify-content: center;
            }
            .st-key-completion-screen div.st-key-reset-game button {
                width: auto !important;
                min-width: 10rem;
            }
            """
        )
    for index in range(len(ANSWER)):
        cell_background = (
            CORRECT_BACKGROUND
            if index in st.session_state.revealed
            else BUTTON_BACKGROUND
        )
        border = "#0ea5e9" if index == st.session_state.active_cell else "#7dd3fc"
        css.append(
            f"""
            div.st-key-cell-{index} button {{
                background: {cell_background} !important;
                color: #ffffff !important;
                border: 2px solid {border} !important;
                min-height: 3rem;
                font-weight: 800;
            }}
            div.st-key-cell-{index} button p {{
                color: #ffffff !important;
            }}
            div.st-key-cell-{index} button:hover,
            div.st-key-cell-{index} button:focus {{
                background: {cell_background} !important;
                border-color: #0ea5e9 !important;
                color: #ffffff !important;
            }}
            """
        )

    for index in range(4):
        background = BUTTON_BACKGROUND
        if (
            st.session_state.answer_state == "wrong"
            and st.session_state.selected_choice == index
        ):
            background = WRONG_BACKGROUND
        elif (
            st.session_state.answer_state == "correct"
            and st.session_state.selected_choice == index
        ):
            background = CORRECT_BACKGROUND
        css.append(
            f"""
            div.st-key-choice-{index} button {{
                background: {background} !important;
                color: #ffffff !important;
                border: 1px solid {background} !important;
                min-height: 5rem;
                white-space: normal;
                height: auto;
                padding: .75rem;
                font-weight: 600;
            }}
            div.st-key-choice-{index} button p {{
                color: #ffffff !important;
                white-space: normal !important;
                overflow: visible !important;
                text-overflow: clip !important;
            }}
            div.st-key-choice-{index} button:hover,
            div.st-key-choice-{index} button:focus {{
                background: {background} !important;
                color: #ffffff !important;
                border-color: #0ea5e9 !important;
            }}
            """
        )
    st.markdown("\n".join(css), unsafe_allow_html=True)


def select_cell(cell_index: int) -> None:
    st.session_state.active_cell = cell_index
    st.session_state.selected_choice = None
    st.session_state.answer_state = None
    st.session_state.feedback = ""


def select_choice(choice_index: int) -> None:
    cell_index = st.session_state.active_cell
    if cell_index is None:
        return

    st.session_state.selected_choice = choice_index
    question = QUESTIONS[cell_index]
    if choice_index == question.correct_choice:
        st.session_state.revealed.add(cell_index)
        st.session_state.answer_state = "correct"
        st.session_state.feedback = "✓ Chính xác!"
        if len(st.session_state.revealed) == len(ANSWER):
            st.session_state.active_cell = None
    else:
        st.session_state.answer_state = "wrong"
        st.session_state.feedback = "✗ Chưa chính xác. Hãy thử đáp án khác nhé!"


def restart_game() -> None:
    st.session_state.revealed = set()
    st.session_state.active_cell = None
    st.session_state.selected_choice = None
    st.session_state.answer_state = None
    st.session_state.feedback = ""


def render_game() -> None:
    st.set_page_config(
        page_title="Minigame - Món quà ý nghĩa",
        page_icon="🎁",
        layout="wide",
    )
    validate_puzzle()
    initialize_state()
    completed = (
        len(st.session_state.revealed) == len(ANSWER)
        and st.session_state.active_cell is None
    )
    render_styles(completed)

    if completed:
        with st.container(key="completion-screen"):
            if COMPLETION_IMAGE.is_file():
                st.image(str(COMPLETION_IMAGE), width="stretch")
            else:
                st.warning(
                    f"Không tìm thấy ảnh chúc mừng mặc định: {COMPLETION_IMAGE}"
                )
            if st.button("Chơi lại", key="reset-game"):
                restart_game()
                st.rerun()
        return

    st.markdown(
        '<h1 class="game-title">MINIGAME TÊN MÓN QUÀ CỰC, CỰC KỲ Ý NGHĨA</h1>'
        '<p class="game-subtitle">Chọn lần lượt các câu hỏi được đánh số từ 1 đến 12.</p>',
        unsafe_allow_html=True,
    )

    with st.container(key="game-panel", border=True):
        st.subheader("12 CÂU HỎI")
        st.write("Chọn số hoặc ô chữ tương ứng để mở câu hỏi.")

        cell_columns = st.columns(len(ANSWER), gap="small")
        for cell_index, column in enumerate(cell_columns):
            with column:
                cell_text = (
                    ANSWER[cell_index]
                    if cell_index in st.session_state.revealed
                    else str(cell_index + 1)
                )
                st.button(
                    cell_text,
                    key=f"cell-{cell_index}",
                    use_container_width=True,
                    on_click=select_cell,
                    args=(cell_index,),
                )

        st.progress(
            len(st.session_state.revealed) / len(ANSWER),
            text=f"Đã hoàn thành {len(st.session_state.revealed)}/{len(ANSWER)} câu",
        )

        if st.session_state.active_cell is not None:
            cell_index = st.session_state.active_cell
            question = QUESTIONS[cell_index]
            st.markdown("---")
            st.markdown(
                f"### Câu {cell_index + 1}: {question.clue}",
                help="Chọn một đáp án bên dưới.",
            )
            answer_columns = st.columns(2, gap="medium")
            for choice_index, choice in enumerate(question.choices):
                with answer_columns[choice_index % 2]:
                    st.button(
                        f"{'ABCD'[choice_index]}. {choice}",
                        key=f"choice-{choice_index}",
                        use_container_width=True,
                        on_click=select_choice,
                        args=(choice_index,),
                    )

            if st.session_state.answer_state == "wrong":
                st.error(st.session_state.feedback)
            elif st.session_state.answer_state == "correct":
                st.success(st.session_state.feedback)
            elif cell_index in st.session_state.revealed:
                st.info("Câu này đã được trả lời đúng. Bạn có thể làm lại câu này.")

        if st.button("Chơi lại", key="reset-game", use_container_width=True):
            restart_game()
            st.rerun()


if __name__ == "__main__":
    render_game()
