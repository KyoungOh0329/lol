const express = require('express'); // Express 웹 프레임워크를 가져옴
const fetch = require('node-fetch'); // node-fetch 모듈을 가져옴
const fs = require('fs'); // 파일 시스템 모듈을 가져옴
const { spawn } = require('child_process'); // child_process 모듈에서 spawn 함수를 가져옴

const app = express(); // Express 애플리케이션 생성
const PORT = 4000; // 서버 포트 설정

app.use(express.static('public')); // public 디렉토리의 정적 파일을 제공
app.use(express.urlencoded({ extended: true })); // URL 인코딩된 요청 처리

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html'); // index.html 파일을 응답으로 보냄
});

app.post('/getMatchData', async (req, res) => {
  try {
    const summonerName = req.body.summonerName; // POST 요청에서 summonerName을 가져옴
    const apiKey = "RGAPI-70faa0cc-7a6f-4d8c-9ef0-a790d1bd776e"; // Riot Games API 키를 입력하세요

    const summonerURL = `https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/${summonerName}?api_key=${apiKey}`; // 소환사 정보를 가져오기 위한 URL 생성

    // 소환사 정보 가져오기
    const summonerResponse = await fetch(summonerURL); // 소환사 정보를 요청
    const summonerData = await summonerResponse.json(); // JSON 형태로 변환

    // puuid 추출
    const puuid = summonerData.puuid; // puuid 추출

    console.log('puuid:', puuid); // puuid 출력

    const matchURL = `https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/${puuid}/ids?start=0&count=1&api_key=${apiKey}`; // 매치 데이터를 가져오기 위한 URL 생성

    // 매치 데이터 가져오기
    const matchResponse = await fetch(matchURL); // 매치 데이터를 요청
    const matchData = await matchResponse.json(); // JSON 형태로 변환

    const matchId = matchData[0]; // 첫 번째 매치 ID 가져오기

    console.log('matchId:', matchId); // matchId 출력

    // matchId를 CSV 파일로 저장
    saveMatchIdToCSV(matchId); // matchId를 CSV 파일에 저장

    res.send(`Match ID received: ${matchId}`); // 응답으로 Match ID 전송
  } catch (error) {
    console.error("API 요청 실패:", error); // 에러 처리
    res.status(500).json({ error: "API 요청 실패" }); // 500 에러 응답
  }
});

function saveMatchIdToCSV(matchId) {
  const csvRow = `${matchId}\n`; // CSV 행 생성

  fs.readFile('Game_id.csv', 'utf8', (err, data) => { // Game_id.csv 파일 읽기
    if (err && err.code !== 'ENOENT') { // 에러 처리
      console.error('Error reading Game_id.csv file:', err);
      return;
    }

    const newCSVData = `Game_id\n${matchId}`; // 새로운 CSV 데이터 생성

    fs.writeFile('Game_id.csv', newCSVData, (err) => { // Game_id.csv 파일 쓰기
      if (err) { // 에러 처리
        console.error('Error writing to CSV file:', err);
      } else {
        console.log('Match ID saved to Game_id.csv'); // Match ID가 Game_id.csv에 저장되었음을 출력
        runPythonScript(); // Python 스크립트 실행
      }
    });
  });
}

function runPythonScript() {
  const pythonProcess = spawn('python3', ['match.py']); // Python 스크립트 실행

  pythonProcess.stdout.on('data', (data) => { // 표준 출력 이벤트 리스너
    console.log(`Python script output: ${data}`); // Python 스크립트 출력 로그
  });

  pythonProcess.stderr.on('data', (data) => { // 표준 에러 이벤트 리스너
    console.error(`Python script error: ${data}`); // Python 스크립트 에러 로그
  });

  pythonProcess.on('close', (code) => { // 종료 이벤트 리스너
    console.log(`Python script process exited with code ${code}`); // Python 스크립트 종료 코드 로그
  });
}

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`); // 서버 시작 메시지 출력
});
