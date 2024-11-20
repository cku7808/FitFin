<template>
    <div>
      <label for="sido">특별시 / 광역시 / 도 : </label>
      <input type="text" name="sido" v-model="siDo" style="width: 300px; margin-bottom: 10px;"/>
      
      <label for="sigungu">시 / 군 / 구 : </label>
      <input type="text" name="sigungu" v-model="siGunGu" style="width: 300px; margin-bottom: 10px;"/>
      
      <label for="eupmyeondong">읍 / 면 / 동 : </label>
      <input type="text" name="eupmyeondong" v-model="eupMyeonDong" style="width: 300px; margin-bottom: 10px;"/>
      
      
      <button @click="searchAddressAndBanks(addressInput)">주소 검색</button>
      <div ref="mapContainer" style="width: 100%; height: 70vh"></div>
    </div>
  </template>
  

<script setup>
import { ref, onMounted, computed } from "vue";

// Kakao Map API Key
const VITE_KAKAO_MAP_KEY = "242327ad0274c1e85ab4064278373781";

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

const addressInput = computed(() => {
    const inputLength = siDo.value.length + siGunGu.value.length + eupMyeonDong.value.length
    if (inputLength === 0) {
        return "서울특별시 역삼동"
    } else {
        return siDo.value + siGunGu.value + eupMyeonDong.value
    }
})

console.log(addressInput)

// Kakao Map API 로드 및 초기화
onMounted(() => {
  loadKakaoMap();
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
    });
  };
};

const initMap = () => {
  const options = {
    center: new kakao.maps.LatLng(33.450701, 126.570667), // 지도 중심 좌표
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
    }
  }, {page: 3});
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
      const markerPositions = data.map((place) => [place.y, place.x]);
      displayMarker(markerPositions);
    } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
      console.warn("근처에 검색된 은행이 없습니다.");
    } else {
      console.error("은행 검색 실패:", status);
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
    markers.value = positions.map(
      (position) =>
        new kakao.maps.Marker({
          map: mapInstance.value,
          position,
        })
    );

    // 지도 범위 설정
    const bounds = positions.reduce(
      (bounds, latlng) => bounds.extend(latlng),
      new kakao.maps.LatLngBounds()
    );

    mapInstance.value.setBounds(bounds);
  }
};
</script>

<style scoped>
</style>
