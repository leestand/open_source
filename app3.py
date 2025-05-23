import streamlit as st
import os
import json
import numpy as np
from supabase import create_client
from openai import OpenAI

# 페이지 구성
st.set_page_config(page_title="건축자재 시맨틱 검색", layout="wide")

# Streamlit에서 실행 중인지 확인하고 secrets 가져오기
try:
    # Streamlit Cloud 환경에서는 st.secrets 사용
    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_key = st.secrets["SUPABASE_KEY"]
    openai_api_key = st.secrets["OPENAI_API_KEY"]
except Exception as e:
    # 로컬 환경에서는 환경 변수 사용
    try:
        import dotenv
        dotenv.load_dotenv()
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_KEY")
        openai_api_key = os.environ.get("OPENAI_API_KEY")
    except:
        st.error("API 키를 가져오는 데 실패했습니다. 환경 변수나 Streamlit Secrets가 제대로 설정되었는지 확인하세요.")
        st.stop()

# API 키 확인
if not supabase_url or not supabase_key or not openai_api_key:
    st.error("필요한 API 키가 설정되지 않았습니다.")
    st.stop()

# Supabase 클라이언트 초기화
try:
    supabase = create_client(supabase_url, supabase_key)
    st.sidebar.success("Supabase 연결 성공!")
except Exception as e:
    st.error(f"Supabase 연결 중 오류가 발생했습니다: {str(e)}")
    st.stop()

# OpenAI 클라이언트 초기화
try:
    openai_client = OpenAI(api_key=openai_api_key)
    st.sidebar.success("OpenAI 연결 성공!")
except Exception as e:
    st.error(f"OpenAI 연결 중 오류가 발생했습니다: {str(e)}")
    st.stop()

def generate_embedding(text):
    """텍스트에서 OpenAI 임베딩 생성"""
    try:
        response =재 블로그 시맨틱 검색")
st.write("Supabase 벡터 데이터베이스에 저장된 안성탕면 관련 블로그 데이터를 시맨틱 검색합니다.")

# 검색 설정 UI
st.sidebar.title("검색 설정")

# 검색 입력
query = st.text_input("검색어 입력", value="안성탕면", help="검색할 키워드나 문장을 입력하세요")

col1, col2 = st.columns(2)
with col1:
    limit = st.slider("검색 결과 수", min_value=1, max_value=50, value=10)
with col2:
    threshold = st.slider("유사도 임계값", min_value=0.0, max_value=1.0, value=0.5, step=0.01)

# 검색 버튼
if st.button("검색", key="search_button"):
    if query:
        with st.spinner("검색 중..."):
            try:
                results = semantic_search(query, limit=limit, match_threshold=threshold)
                
                if results:
                    st.success(f"{len(results)}개의 결과를 찾았습니다.")
                    
                    # 결과 표시
                    for i, result in enumerate(results):
                        similarity = result['similarity'] * 100  # 백분율로 변환
                        
                        # 메타데이터에서 정보 추출
                        metadata = result.get('metadata', {})
                        title = metadata.get('title', '제목 없음')
                        
                        # 블로그 URL 추출 (메타데이터 구조에 따라 다르게 처리)
                        url = None
                        if 'url' in metadata:
                            url = metadata['url']
                        
                        # 결과 표시
                        with st.expander(f"{i+1}. {title} (유사도: {similarity:.2f}%)"):
                            st.write(f"**내용:** {result['content'][:300]}...")
                            
                            # 메타데이터 정보 표시
                            meta_col1, meta_col2 = st.columns(2)
                            
                            with meta_col1:
                                if 'bloggername' in metadata:
                                    st.write(f"**블로그:** {metadata['bloggername']}")
                                if 'date' in metadata:
                                    st.write(f"**날짜:** {metadata['date']}")
                            
                            with meta_col2:
                                if url:
                                    st.markdown(f"**링크:** [원본 글 보기]({url})")
                                if 'collection' in metadata:
                                    st.write(f"**컬렉션:** {metadata['collection']}")
                else:
                    st.warning("검색 결과가 없습니다. 다른 검색어를 시도해보세요.")
            
            except Exception as e:
                st.error(f"검색 중 오류가 발생했습니다: {str(e)}")
    else:
        st.warning("검색어를 입력하세요.")

# 데이터베이스 상태
st.sidebar.title("데이터베이스 상태")
try:
    result = supabase.table('documents').select('id', count='exact').execute()
    doc_count = result.count if hasattr(result, 'count') else len(result.data)
    st.sidebar.info(f"저장된 문서 수: {doc_count}개")
except Exception as e:
    st.sidebar.error("데이터베이스 상태를 확인할 수 없습니다.")

# 사용 안내
st.sidebar.title("사용 안내")
st.sidebar.info("""
1. 검색어 입력: 검색하고 싶은 키워드나 문장을 입력하세요.
2. 검색 결과 수: 보고 싶은 결과의 개수를 설정하세요.
3. 유사도 임계값: 검색 결과의 최소 유사도를 설정하세요. 높을수록 더 관련성 높은 결과만 표시됩니다.
""")
