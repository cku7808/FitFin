<template>
  <div class="d-flex flex-column align-items-center score-dream">
    <h2 class="mb-5 score-dream-bold">
      <span class="text-highlight">주변 </span>
      <span>은행 찾기</span>
    </h2>
    <div class="d-flex flex-column col-6 justify-content-center text-center">
      <div class="wrap">
        <div class="radio_area w-50 me-2">
          <input type="radio" name="address" id="address1" value="true" v-model="addressType" checked>
          <label for="address1"><span></span>행정 구역 별 입력</label>&nbsp
        </div>
        <div class="radio_area w-50 ms-2">
          <input type="radio" name="address" id="address2" value="false" v-model="addressType">
          <label for="address2"><span></span>도로명 주소 입력</label>  
        </div>  
      </div>

      <div v-if="addressType === 'true'" class="d-flex justify-content-evenly">
        <input type="text" name="sido" v-model="siDo" style=" margin-bottom: 10px;" placeholder="특별시/광역시/도" class="form-control "/>&nbsp
        <input type="text" name="sigungu" v-model="siGunGu" style=" margin-bottom: 10px;" placeholder="시/군/구" class="form-control "/>&nbsp
        <input type="text" name="eupmyeondong" v-model="eupMyeonDong" style=" margin-bottom: 10px;" placeholder="읍/면/동" class="form-control "/>&nbsp
      </div>
      <div v-else class="text-center">
        <input type="text" name="doro" v-model="doro" style="width: 100%; margin-bottom: 10px;" placeholder="도로명 주소" class="form-control "/>
      </div>
      <br>
      <button class="button" @click="searchAddressAndBanks(addressInput)">주소 검색</button>
      <br>
    </div>
      <div ref="mapContainer" style="width: 60%; height: 70vh;" class="card-1">
        
      </div>
      <br>
  </div>
  </template>
  

<script setup>
import { ref, onMounted, computed } from "vue";
import markerImageSrc from '/map/marker3.png';

// Kakao Map API Key
const VITE_KAKAO_MAP_KEY = import.meta.env['VITE_API_KEY_KAKAO_JS']

const addressType = ref('true')
console.log(addressType)
// 상태 관리
const mapContainer = ref(null);
const mapInstance = ref(null);
const placesService = ref(null); // 장소 검색 서비스
const markers = ref([]);
const geocoder = ref(null); // Geocoder 인스턴스
// const addressInput = ref('서울특별시 역삼동')

// 특별시, 광역시, 도
const siDo = ref('')
// 시, 군, 구
const siGunGu = ref('')
// 읍, 면, 동
const eupMyeonDong = ref('')
// 도로명 주소
const doro = ref('')

const addressInput = computed(() => {
  if (addressType.value === 'true'){
    const inputLength = siDo.value.length + siGunGu.value.length + eupMyeonDong.value.length
    if (inputLength !== 0) {
      return siDo.value + siGunGu.value + eupMyeonDong.value
    }
  } else {
    const inputLength = doro.value
    if (inputLength !== 0) {
      return doro.value
    }
  }
})

const currentLatitude = ref('')
const currentLongitude = ref('')

// 내 현재 위치 찾기 
navigator.geolocation.getCurrentPosition((position) => {
  currentLatitude.value = position.coords.latitude
  currentLongitude.value = position.coords.longitude
})

// Kakao Map API 로드 및 초기화
onMounted(() => {
  loadKakaoMap()
});

const loadKakaoMap = () => {
  const script = document.createElement("script");
  script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${VITE_KAKAO_MAP_KEY}&autoload=false&libraries=services,clusterer,drawing`;
  document.head.appendChild(script);

  script.onload = () => {
    window.kakao.maps.load(() => {
      initMap();
      initGeocoder();
      initPlacesService(); // Places 라이브러리 초기화
      searchCurrentPosBanks();
    });
  };
};

const initMap = () => {
  const options = {
    center: new kakao.maps.LatLng(currentLatitude.value, currentLongitude.value), // 지도 중심 좌표
    level: 5, // 초기 확대 레벨
    maxLevel: 10, // 최대 축소 레벨
  };
  mapInstance.value = new kakao.maps.Map(mapContainer.value, options);
};

const initGeocoder = () => {
  geocoder.value = new kakao.maps.services.Geocoder();
};

const initPlacesService = () => {
  placesService.value = new kakao.maps.services.Places();
};

// 주소를 검색하고 해당 위치 근처의 은행 정보를 찾는 함수
const searchAddressAndBanks = async (address) => {
  if (!geocoder.value || !placesService.value) return;

  // 주소 검색
  geocoder.value.addressSearch(address, (result, status) => {
    if (status === kakao.maps.services.Status.OK) {
      console.log("주소 검색 결과:", result);

      // 첫 번째 결과의 좌표로 지도 이동
      const { x, y } = result[0];
      const position = new kakao.maps.LatLng(y, x);
      mapInstance.value.setCenter(position);

      // 은행 검색
      searchNearbyBanks(position);
    } else {
      console.error("주소 검색 실패:", status);
      alert('주소 정보가 올바르지 않습니다.')
    }
  });
};

// 현재 위치 근처의 은행 정보를 찾는 함수
const searchCurrentPosBanks = async () => {
  if (!geocoder.value || !placesService.value) return;

  // 첫 번째 결과의 좌표로 지도 이동
  const x = currentLongitude.value;
  const y = currentLatitude.value;
  const position = new kakao.maps.LatLng(y, x);
  mapInstance.value.setCenter(position);

  // 은행 검색
  searchNearbyBanks(position);
};

// 특정 좌표 근처의 은행을 검색하는 함수
const searchNearbyBanks = (position) => {
  if (!placesService.value) return;
  
  const placesOptions = {
    location: position,
    radius: 1000, // 검색 반경 (1km)
    category_group_code: "BK9", // 은행 카테고리 코드
  };

  placesService.value.keywordSearch("은행", (data, status) => {
    if (status === kakao.maps.services.Status.OK) {
      console.log("근처 은행 검색 결과:", data);

      // 검색 결과로 마커 표시
      const markerPositions = data.map((place) => [place.y, place.x, place.address_name, place.place_name]);
      displayMarker(markerPositions);
    } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
      console.warn("근처에 검색된 은행이 없습니다.");
    } else {
      console.error("은행 검색 실패:", status);
      alert('검색된 은행이 없습니다')
    }
  }, placesOptions);
};

// 마커 표시 함수
const displayMarker = (markerPositions) => {
  // 기존 마커 제거
  if (markers.value.length > 0) {
    markers.value.forEach((marker) => marker.setMap(null));
    markers.value = [];
  }

  // 새 마커 추가
  const positions = markerPositions.map(
    (position) => new kakao.maps.LatLng(...position)
  );

  if (positions.length > 0) {
    markers.value = positions.map((position, index) => {
      const imageSize = new kakao.maps.Size(40, 40) // 마커 이미지 크기
      const imageOption = { offset: new kakao.maps.Point(20, 40) } // 이미지 기준점

      const markerImage = new kakao.maps.MarkerImage(markerImageSrc, imageSize, imageOption);

      const marker = new kakao.maps.Marker({
        map: mapInstance.value,
        position: position,
        image: markerImage,
      })
      displayCustomOverlay(marker, markerPositions[index][2], markerPositions[index][3]);
      return marker
    });

    // 지도 범위 설정
    const bounds = positions.reduce(
      (bounds, latlng) => bounds.extend(latlng),
      new kakao.maps.LatLngBounds()
    );

    mapInstance.value.setBounds(bounds);
  }
}
const displayCustomOverlay = (marker, placeAddress, placeName) => {
  // 마커 클릭 이벤트
  kakao.maps.event.addListener(marker, "click", () => {
    // 기존 오버레이 닫기
    closeAllOverlays();

    // 오버레이 내용 생성
    const content = `
      <div style="position: relative; bottom: 80px; padding: 10px; background-color: white; border: 1px solid #ccc; border-radius: 6px; box-shadow: 0 2px 6px rgba(0,0,0,0.3); white-space: nowrap;">
        <p style="margin: 0; font-size: 14px; font-weight: bold;">${placeName}</p>
        <p style="margin: 0; font-size: 12px; color: gray;">${placeAddress}</p>
        <div style="margin-top: 5px; text-align: right;">
          <button style="padding: 3px 8px; font-size: 12px; color: white; background-color: #60BF78; border: none; border-radius: 4px; cursor: pointer;" onclick="closeOverlay()">닫기</button>
        </div>
      </div>
    `;

    // CustomOverlay 생성
    const overlay = new kakao.maps.CustomOverlay({
      map: mapInstance.value,
      position: marker.getPosition(),
      content,
      yAnchor: 0.7, // 커스텀 오버레이의 y축 앵커 (마커 위로 표시)
    });

    // 현재 열린 오버레이 저장
    currentOverlay.value = overlay;

    // 닫기 버튼 클릭 시 오버레이 닫기
    window.closeOverlay = () => {
      closeAllOverlays();
    };
  });
};

// 현재 열린 오버레이를 추적
const currentOverlay = ref(null);

// 모든 오버레이 닫기
const closeAllOverlays = () => {
  if (currentOverlay.value) {
    currentOverlay.value.setMap(null);
    currentOverlay.value = null;
  }
};


</script>

<style scoped>
  @font-face {
    font-family: 'S-CoreDream-3Light';
    src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_six@1.2/S-CoreDream-3Light.woff') format('woff');
    font-weight: normal;
    font-style: normal;
  }
  .score-dream {
    font-family: 'S-CoreDream-3Light';
  }
  .score-dream-bold {
  font-family: 'S-CoreDream-3Light';
  font-weight: bold;
}
input:focus {
    border: 1px solid #79F297 !important;
    box-shadow: none !important;
    background-color: transparent !important;
  }
input:active {
  background-color: inherit !important; 
  border: 1px solid #79F297 !important;
  box-shadow: none !important;
}
.form-select:focus {
    border: 1px solid #79F297 !important;
    box-shadow: none !important;
  }
.form-select:active {
  background-color: inherit !important; 
  border: 1px solid #79F297 !important;
  box-shadow: none !important;}
.form-control {
  margin-bottom: 0px !important;
}
.button {
  background-color: #203359;
  border: none;
  color: white;
  border-radius: 10px;
  height: 30px;
}
.wrap {display:flex;flex-flow:row;justify-content: center;gap:5px;}

.wrap .radio_area label{cursor:pointer;display:flex;align-items:center;gap:15px;height:40px;padding:0 18px 0 15px;border-radius:30px;font-size:15px;font-weight:500;color:#999;background:#f2f2f2;transition:all .2s}
.wrap .radio_area label span{opacity:.3;display:flex;width:18px;height:18px;border:2px solid #2d3e50;border-radius:50%;transition:all .2s}
.wrap .radio_area label span:before{content:"";width:6px;height:6px;margin:auto;border-radius:50%;background:#2d3e50;transition:all .2s}
.wrap .radio_area label:hover{background:#e1e1e1}
.radio_area input[type=radio]{display:none}
.radio_area input[type=radio]:checked + label{color:#79F297;background:#2d3e50}
.radio_area input[type=radio]:checked + label span{opacity:1;border-color:#79F297}
.radio_area input[type=radio]:checked + label span:before{background:#79F297}
.text-highlight{
    color: #79F297;
}
.card-1 {
  box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
  transition: all 0.3s cubic-bezier(.25,.8,.25,1);
  border-radius: 10px;
}

.card-1:hover {
  box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
}
</style>
