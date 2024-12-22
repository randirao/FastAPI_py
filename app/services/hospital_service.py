import folium
import json
import requests
import os
from dotenv import load_dotenv
from typing import Dict, List
from folium.plugins import MarkerCluster

# .env 파일 로드
load_dotenv()

def get_hospitals_from_api() -> List[Dict]:
    """공공데이터 포털에서 부산 지역 병원 정보를 가져옵니다."""
    url = "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"
    
    service_key = os.getenv('HOSPITAL_API_KEY')
    
    params = {
        'serviceKey': service_key,
        'pageNo': '1',
        'numOfRows': '100',
        'sidoCd': '26',      # 부산광역시 코드
        '_type': 'json'
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data['response']['body']['items']['item']
    except Exception as e:
        print(f"Error fetching hospital data: {e}")
        return []

def generate_hospital_map():
    # 부산 중심 좌표
    map_center = [35.1796, 129.0756]
    m = folium.Map(location=map_center, zoom_start=12)
    
    # 마커 클러스터 생성
    marker_cluster = MarkerCluster().add_to(m)
    
    try:
        hospitals = get_hospitals_from_api()
        
        for hospital in hospitals:
            try:
                lat = float(hospital.get('YPos', 0))
                lon = float(hospital.get('XPos', 0))
                name = hospital.get('yadmNm', '병원명 없음')
                addr = hospital.get('addr', '주소 없음')
                tel = hospital.get('telno', '전화번호 없음')
                
                if lat and lon:
                    # 커스텀 아이콘 HTML
                    custom_icon_html = f"""
                        <div style="position: relative;">
                            <div style="
                                width: 20px;
                                height: 20px;
                                background-color: #FF4B4B;
                                border: 3px solid white;
                                border-radius: 50%;
                                box-shadow: 0 0 15px rgba(0,0,0,0.3);
                            "></div>
                            <div style="
                                position: absolute;
                                top: 50%;
                                left: 50%;
                                transform: translate(-50%, -50%);
                                color: white;
                                font-weight: bold;
                                font-size: 14px;
                            ">+</div>
                        </div>
                    """
                    
                    # 팝업 내용
                    popup_html = f"""
                        <div style="
                            font-family: 'Malgun Gothic', sans-serif;
                            padding: 10px;
                            min-width: 200px;
                        ">
                            <h3 style="
                                color: #FF4B4B;
                                margin: 0 0 10px 0;
                                border-bottom: 2px solid #FF4B4B;
                                padding-bottom: 5px;
                            ">{name}</h3>
                            <p style="margin: 5px 0;"><strong>주소:</strong><br>{addr}</p>
                            <p style="margin: 5px 0;"><strong>📞 전화:</strong><br>{tel}</p>
                        </div>
                    """
                    
                    # 마커 추가
                    folium.Marker(
                        location=[lat, lon],
                        popup=folium.Popup(popup_html, max_width=300),
                        icon=folium.DivIcon(
                            html=custom_icon_html,
                            icon_size=(20, 20),
                            icon_anchor=(10, 10)
                        )
                    ).add_to(marker_cluster)
            
            except (ValueError, TypeError) as e:
                continue

    except Exception as e:
        print(f"Error creating map: {e}")
    
    return m._repr_html_()