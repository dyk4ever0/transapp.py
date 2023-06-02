import streamlit as st
from translate_docx import translate_docx
from glossary_database import add_entry, remove_entry, get_glossary
import os

def save_uploaded_file(upload):
    try:
        with open(os.path.join('uploads', upload.name), 'wb') as f:
            f.write(upload.getvalue())
        return 1
    except Exception as e:
        print(e)
        return 0

def glossary_management():
    st.header('🏭 용어집 관리')
    st.write('용어집은 {한국어:영어} 단어 쌍으로 구성되며, 오번역된 문장을 교정하는 데 사용됩니다.')
    st.write('#### 현재 등록 용어집')
    glossary = get_glossary()
    st.write(glossary)
    # Allow user to add a new entry
    st.write('#### 새 용어 추가하기')
    st.write('등록하신 후 기다리면 용어집에 자동 반영됩니다.')
    korean_word = st.text_input('한국어')
    english_word = st.text_input('영문 번역')
    if st.button('등록'):
        add_entry(korean_word, english_word)
        st.success('추가되었습니다')

    # Allow user to remove an entry
    st.write('#### 용어 삭제하기')
    korean_word_to_remove = st.text_input('삭제할 한국어 용어')
    if st.button('삭제'):
        remove_entry(korean_word_to_remove)
        st.success('삭제되었습니다')

def translate_document():
    st.title('💌 워드 파일 문서 번역기')

    uploaded_file = st.file_uploader(".docx 파일을 업로드해주세요.", type='docx')

    if uploaded_file is not None:
        if save_uploaded_file(uploaded_file):
            with st.spinner(text='Translating document...'):
                translated_filename = translate_docx(os.path.join('uploads', uploaded_file.name))
            if translated_filename:
                st.success('번역 완료')
                with open(translated_filename, 'rb') as f:
                    st.download_button(
                        label="Download Translated Document",
                        data=f,
                        file_name="translated_document.docx",
                        mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    )
            else:
                st.error('번역 실패')
        else:
            st.error('파일 저장 실패')

def main():
    with st.sidebar:
        st.title('💌 문서 번역 사이트')
        st.markdown(''' #### ⛳︎ DeepL을 통해 문서를 번역하는 사이트입니다.''')
        st.markdown(f'<p style="font-size:14px;">번역본을 다운로드 하신 후에는 반드시 검토해주세요.', unsafe_allow_html=True)
        st.write('')
        st.write('')
        # add_selectbox = st.sidebar.selectbox(
        #     "※사용하실 번역 종류를 선택해주세요.",
        #     ("한❯영 번역", "한❯한+영 병기 번역")
        # )
        st.write('---')
        page = st.sidebar.selectbox("사용하실 페이지를 선택하세요", ["💌 문서 번역", "🏭 용어집 관리"])
    if page == "💌 문서 번역":
        translate_document()
    elif page == "🏭 용어집 관리":
        glossary_management()


def glossary_management():
    st.title('🏭 용어집 관리')
    st.write('#### 현재 등록 용어집')

    filter_option = st.selectbox("용어 보기:", ('전체', '영어 A-Z'))
    glossary = get_glossary()

    # if filter_option == '한국어 ㄱ-ㅎ':
    #     korean_consonants = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    #     korean_consonant = st.selectbox("시작 자음 선택:", korean_consonants)
    #     filtered_glossary = {k: v for k, v in glossary.items() if k[0] == korean_consonant}
    if filter_option == '영어 A-Z':
        english_alphabet = st.selectbox("Select Starting Letter:", [chr(i) for i in range(ord('A'), ord('Z')+1)])
        filtered_glossary = {k: v for k, v in glossary.items() if v[0].upper() == english_alphabet}
    else:
        filtered_glossary = glossary

    st.write(filtered_glossary)

    # Allow user to add a new entry
    st.write('#### 새 용어 추가하기')
    korean_word = st.text_input('한국어')
    english_word = st.text_input('영문 번역')
    if st.button('등록'):
        add_entry(korean_word, english_word)
        st.success('추가되었습니다')

    # Allow user to remove an entry
    st.write('#### 용어 삭제하기')
    korean_word_to_remove = st.text_input('삭제할 용어')
    if st.button('삭제'):
        remove_entry(korean_word_to_remove)
        st.success('삭제되었습니다')



if __name__ == "__main__":
    main()

