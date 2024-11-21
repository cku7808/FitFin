<template>
    <div>
      <fieldset>
        <input type="radio" name="address" value="true" v-model="addressType" checked>
        <label for="">행정 구역 별 입력</label>&nbsp

        <input type="radio" name="address" value="false" v-model="addressType">
        <label for="">도로명 주소 입력</label>
      </fieldset>

      <div v-if="addressType === 'true'">
        <label for="sido">특별시 / 광역시 / 도 : </label>
        <input type="text" name="sido" v-model="siDo" style="width: 300px; margin-bottom: 10px;"/>
        
        <label for="sigungu">시 / 군 / 구 : </label>
        <input type="text" name="sigungu" v-model="siGunGu" style="width: 300px; margin-bottom: 10px;"/>
        
        <label for="eupmyeondong">읍 / 면 / 동 : </label>
        <input type="text" name="eupmyeondong" v-model="eupMyeonDong" style="width: 300px; margin-bottom: 10px;"/>
      </div>
      <div v-else>
        <label for="sido">도로명 주소 : </label>
        <input type="text" name="doro" v-model="doro" style="width: 300px; margin-bottom: 10px;"/>
      </div>
      
      
      <button @click="searchAddressAndBanks(addressInput)">주소 검색</button>
      <div ref="mapContainer" style="width: 100%; height: 70vh"></div>
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

</style>
