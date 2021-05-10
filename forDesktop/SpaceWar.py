# -*- coding: utf-8-*-

import pygame
import random
import time
import sys

gameWidth = 480
gameHeight = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (244, 67, 54)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 244, 143)

# 파일경로
# todo : 파일경로 설정
background = 'backgroundMusic/'
font = 'font/'
images = 'images/'
soundEffect = 'soundEffect/'

# pygame 초기화
pygame.init()

# 전체화면으로 설정
screen = pygame.display.set_mode((gameWidth, gameHeight))
clock = pygame.time.Clock()  # FPS 설정 변수
pygame.mouse.set_visible(False)  # 마우스 포인터 삭제

# font
gameFont24 = pygame.font.Font(font + 'Starjedi.ttf', 24)  # 'score' 숫자 출력 폰트
numberFont16 = pygame.font.Font(font + 'malgunbd.ttf', 16)  # 'money' 숫자 출력 폰트
numberFont20 = pygame.font.Font(font + 'malgunbd.ttf', 20)  # 'money' 숫자 출력 폰트

# images
playerExplosion = pygame.image.load(images + 'player_explosion.png')  # player 폭발 이미지
playerHit = pygame.image.load(images + 'player_hit.png')  # player hit 이미지
lifeImage = pygame.image.load(images + 'life.png')  # 생명 이미지
missileImage = pygame.image.load(images + 'missile.png')  # 미사일 이미지
moneyBag = pygame.image.load(images + 'moneybag.png')  # 돈주머니 이미지
moneyUp = pygame.image.load(images + 'moneyup.png')  # 돈 얻는 이미지
nuclearMissileImage = pygame.image.load(images + 'nuclear_missile.png')  # 핵 미사일 이미지
bossExplosion01 = pygame.image.load(images + 'boss_explosion01.png')  # 보스 폭발 효과1
bossExplosion02 = pygame.image.load(images + 'boss_explosion02.png')  # 보스 폭발 효과2

# background music
startBackgroundMusic = pygame.mixer.Sound(background + 'Powerup.wav')  # 게임 시작화면 배경음악
backgroundMusic = pygame.mixer.Sound(background + 'Epic_Journey.wav')  # 게임 배경음악
stationSound = pygame.mixer.Sound(background + 'station.wav')  # 우주정거장 배경음악

# soundEffect
shootingSound = pygame.mixer.Sound(soundEffect + 'laser_gun.wav')  # 발사 효과음 로드
coinSound = pygame.mixer.Sound(soundEffect + 'coin.wav')  # 돈 효과음 로드
playerHitSound = pygame.mixer.Sound(soundEffect + 'player_hit.wav')  # 플레이어 hit 효과음 로드
playerExplosionSound = pygame.mixer.Sound(soundEffect + 'player_explosion.wav')  # 플레이어 폭발 효과음 로드
ufoExplosionSound = pygame.mixer.Sound(soundEffect + 'ufo_explosion.wav')  # ufo 폭발 효과음 로드
warning = pygame.mixer.Sound(soundEffect + 'warning.wav')  # 핵미사일 경보 효과음
nuclearSound = pygame.mixer.Sound(soundEffect + 'launched_nuclear.wav')  # 핵미사일 날라가는 효과음
nuclearExplosionSound = pygame.mixer.Sound(soundEffect + 'nuclear_explosion.wav')  # 핵미사일 폭발하는 효과음
clickSound = pygame.mixer.Sound(soundEffect + 'click.wav')  # 클릭 효과음
clickSound2 = pygame.mixer.Sound(soundEffect + 'click2.wav')  # 클릭 효과음2
buySound = pygame.mixer.Sound(soundEffect + 'buy.wav')  # 구매 효과음
errorSound = pygame.mixer.Sound(soundEffect + 'error.wav')  # 에러 효과음

direction = ['Down', 'Right', 'Left']  # UFO 진행 방향
pattern = ['straight', 'straight', 'leftRight', 'leftRight', 'slow']  # UFO Missile 공격 패턴

# sprite 그룹 설정
playerMissiles = pygame.sprite.Group()  # Player 미사일 그룹
ufos = pygame.sprite.Group()  # UFO 그룹
ufoMissiles = pygame.sprite.Group()  # UFOmissile 그룹
nuclear = pygame.sprite.Group()  # Nuclear 그룹
bossMissiles = pygame.sprite.Group()  # Boss 미사일 그룹

# 게임 진행상황, 환경설정 변수
FPS = 60  # 초당 프레임
spaceshipLevel = 1  # player 레벨
spaceshipCount = str(spaceshipLevel)
roundLevel = 1  # 라운드 레벨
roundCount = str(roundLevel)
missileSpeed = spaceshipLevel + 10  # player 미사일 속도값
missileCount = 0  # player 미사일 카운트 체크 변수
reloadTime = 0.7 - (spaceshipLevel / 10)  # player 미사일 재장전 시간
roundTime = 60  # 라운드 타이머
respawnTime = 5  # UFO 리스폰 타이머
launchTime = 2  # UFO 미사일 발사 간격 시간
moneyLoadTime = 0.5  # 돈 이미지 출력 시간
hitLoadTime = 0.3  # player 히트 이미지 출력 시간
getMoney = 5  # 돈 얻을 확률
money = 0  # 현재 돈
score = 0  # 현재 점수
nuclearCount = 0  # 핵미사일 발사 가능 개수
life = 100  # player 생명
changeDir = False  # 전기 이벤트의 방향을 바꿔주는 변수
imageTime = 0.8  # 이미지 출력 시간


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, spaceshipCount):
        super(Player, self).__init__()
        self.image = pygame.image.load(images + 'spaceship_level' + spaceshipCount + '.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.centerX = self.rect.centerx
        self.centerY = self.rect.centery

    def set_pos(self, x, y):
        self.rect.x = x - self.centerX
        self.rect.y = y - self.centerY

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_mask(self, sprite):
                return sprite

# UFO class
class UFO(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, xspeed, yspeed, missileType, missilePattern, ufoMissileSpeed, ufoMissileStartTime):
        # xpos, ypos, xspeed, yspeed : UFO 오브젝트 이동을 위한 파라미터
        # missileType, missilePattern, ufoMissileSpeed, ufoMissileStartTime : UFO 미사일 발사를 위한 파라미터
        super(UFO, self).__init__()
        # UFO 오브젝트 관련 설정
        ufos = ['ufo01.png', 'ufo02.png', 'ufo03.png', 'ufo04.png']  # missileType = 미사일 레벨
        self.image = pygame.image.load(images + random.choice(ufos)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.centerX = self.rect.centerx
        self.centerY = self.rect.centery
        self.xspeed = xspeed
        self.yspeed = yspeed

        # UFO 미사일 관련 변수
        self.missileType = missileType  # 미사일 이미지
        self.missilePattern = missilePattern  # 미사일 패턴
        self.ufoMissileSpeed = ufoMissileSpeed  # 미사일 속도
        self.ufoMissileStartTime = ufoMissileStartTime  # 미사일 시간측정

    def update(self):
        # UFO 이동
        self.rect.x += self.xspeed
        self.rect.y += self.yspeed

        # UFO 미사일 발사
        # 미사일 발사를 위한 UFO center좌표 업데이트
        self.centerX += self.xspeed
        self.centerY += self.yspeed
        if self.missileLaunch():
            # UFO의 현재 좌표와 미사일 생성을 위한 값들을 ufoMissiles 그룹에 추가
            if self.missilePattern == 'straight':
                # 직선 발사
                ufoMissiles.add(ufoMissile_moving(self.centerX, self.centerY, self.missileType,
                                                  '1', self.ufoMissileSpeed, self.ufoMissileStartTime))

            elif self.missilePattern == 'leftRight':
                # 대각선(->) 발사
                ufoMissiles.add(ufoMissile_moving(self.centerX, self.centerY, self.missileType,
                                                  '2', self.ufoMissileSpeed, self.ufoMissileStartTime))
                # 대각선(<-) 발사
                ufoMissiles.add(ufoMissile_moving(self.centerX, self.centerY, self.missileType,
                                                  '3', self.ufoMissileSpeed, self.ufoMissileStartTime))

            elif self.missilePattern == 'slow':
                # 느리게 발사
                ufoMissiles.add(ufoMissile_moving(self.centerX, self.centerY, self.missileType,
                                                  '4', self.ufoMissileSpeed, self.ufoMissileStartTime))

            self.ufoMissileStartTime = time.time()

        # UFO 오브젝트가 화면 끝까지가면 삭제
        if self.out():
            self.kill()

    def out(self):
        if self.rect.y > gameHeight:  # 아랫쪽으로 사라졌을 때
            return True

        elif self.rect.x < 0 - self.rect.width:  # 오른쪽으로 사라졌을 때
            return True

        elif self.rect.x > gameWidth:  # 왼쪽으로 사라졌을 때
            return True

    # UFO 미사일 발사 코드
    def missileLaunch(self):
        # ufo 미사일 발사 시간 측정 변수
        launchEndTime = time.time()
        launchReasultTime = launchEndTime - self.ufoMissileStartTime

        if launchReasultTime >= launchTime:  # launchTime 이상이면 발사
            return True
        else:
            return False


# UFO Missile class
class UFOMissile(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, missileType, missilePattern, ufoMissileSpeed, ufoMissileStartTime):
        # xpos, ypos : UFO 클래스에서 받아온 UFO의 현재 좌표
        super(UFOMissile, self).__init__()
        self.image = pygame.image.load(images + 'ufoMissile_level' + missileType + '.png')
        self.image2 = pygame.image.load(images + 'energy_missile.png')
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.pattern = missilePattern
        self.speed = ufoMissileSpeed
        self.startTime = ufoMissileStartTime

        self.setDirection()

    def update(self):
        # pattern = 1: 직선 이동
        # pattern = 2: 오른쪽 대각선 이동
        # pattern = 3: 왼쪽 대각선 이동
        # pattern = 4: 느린 미사일
        if self.pattern == '1':
            self.rect.y += self.speed
            # UFO 미사일이 화면 끝까지가면 삭제
            if self.out():
                self.kill()

        elif self.pattern == '2':
            self.rect.x += self.speed / 2
            self.rect.y += self.speed
            if self.out():
                self.kill()

        elif self.pattern == '3':
            self.rect.x -= self.speed / 2
            self.rect.y += self.speed
            if self.out():
                self.kill()

        elif self.pattern == '4':
            self.image = self.image2  # 이미지 교체
            self.rect.y += self.speed / 2.5
            if self.out():
                self.kill()

    def setDirection(self):
        # 오른쪽으로 30도 회전
        if self.pattern == '2':
            self.image = pygame.transform.rotate(self.image, 30)

        # 왼쪽으로 30도 회전
        elif self.pattern == '3':
            self.image = pygame.transform.rotate(self.image, -30)

    def out(self):
        if self.rect.y > gameHeight:
            return True


# Missile class
class Missile(pygame.sprite.Sprite):
    def __init__(self, spaceshipCount, xpos, ypos, speed):
        super(Missile, self).__init__()
        self.image = pygame.image.load(images + 'missile_level' + spaceshipCount + '.png')
        self.rect = self.image.get_rect()
        self.centerX = self.rect.centerx
        self.centerY = self.rect.centery
        self.rect.x = xpos - self.centerX
        self.rect.y = ypos
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        # player 미사일이 화면 끝까지가면 삭제
        if self.out():
            self.kill()

    def out(self):
        if self.rect.y < 0:
            return True


# nuclear missile class
class Nuclear(pygame.sprite.Sprite):
    def __init__(self):
        super(Nuclear, self).__init__()
        self.image = pygame.image.load(images + 'launched_nuclear.png')  # 핵 미사일 발사 이미지
        self.image2 = pygame.image.load(images + 'white.png')
        self.image3 = pygame.image.load(images + 'nuclear_explosion.png')  # 핵 폭발 이미지
        self.rect = self.image.get_rect()
        self.rect.x = 220
        self.rect.y = 850
        self.oneTimeCheck = True
        self.explosionCheck = False
        self.soundCheck = True
        self.soundCheck2 = True

    def update(self):
        if self.rect.y > 200:
            self.rect.y -= 1.5
            if self.rect.y <= 850 and self.soundCheck == True:
                # 사운드를 한번만 재생
                nuclearSound.play()
                self.soundCheck == False

        # y 좌표가 200이 되었을 때 폭발
        if self.rect.y <= 200:
            self.explosionCheck = True
            nuclearSound.stop()

        ''' startTime을 단 한번만 찍기위한 코드
            oneTimeCheck 변수가 False로 바뀌면서 더 이상 이 조건문을 실행하지 않음 '''
        if self.oneTimeCheck == True and self.explosionCheck == True:
            self.oneTimeCheck = False
            self.startTime = time.time()

        if self.explosionCheck == True:
            # 폭발 사운드를 한번만 재생
            if self.soundCheck2 == True:
                nuclearExplosionSound.play()
                self.soundCheck2 == False
            # x, y 좌표값 재조정
            self.rect.x = 0
            self.rect.y = 0
            self.image = self.image2  # 섬광 이미지
            # 이미지를 계속 출력하기 위한 time 함수
            endTime = time.time()
            resultTime = endTime - self.startTime

            ufos.empty()  # 현재 생성된 UFO 모두 삭제
            ufoMissiles.empty()  # 현재 생성된 UFO 미사일 모두 삭제

            # 0.5초 까지는 섬광이미지 출력, 이후로는 폭발 이미지 출력
            if resultTime >= 0.5:
                # x, y 좌표값 재조정
                self.rect.x = -80
                self.rect.y = -50
                self.image2 = self.image3
                # 3.5초가 지났을 때 삭제
                if resultTime >= 4:
                    self.kill()


# Boss Class
class Boss(pygame.sprite.Sprite):
    def __init__(self, level):
        super(Boss, self).__init__()
        self.image = pygame.image.load(images + 'boss0' + level + '.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = - 400  # 화면 안보이는 곳부터 등장하도록
        self.centerX = self.rect.centerx
        self.centerY = self.rect.centery
        self.speed = 1  # 초기 등장용
        self.startTime = time.time()  # 첫발사 시작 시간
        self.MissileStartTime = time.time()  # 미사일 발사 시간
        self.intervalStartTime = time.time()  # 미사일 발사 간격
        self.missileType = level  # 미사일 모양(레벨에 따라 다름)
        self.launchTime = int(level) + 3  # 발사 지속 시간
        self.missilePattern = ['1']  # 패턴(1, 2, 3, 4)
        self.patternCheck = True  # 패턴 변경이 한번만 이루어 지도록 하는 변수
        self.randomPattern = '1'  # 오류 방지용
        self.life = int(level) * 100  # 생명

    def update(self):
        if self.rect.y <= 0:
            self.rect.y += self.speed  # 초기 등장시 위에서부터 아래로 서서히 내려오면서 등장
            self.centerY += self.speed
        else:
            pass  # 일정부분 내려오면 더이상 움직이지 않음

        randomX = random.randint(self.centerX - 220, self.centerX + 220)  # 미사일이 발사되는 X좌표는 랜덤하게

        # 등장후 11초 뒤(missileStart())에 발사(launchStart)
        # 이 조건문은 4초동안 열리고 3초동안 닫히고를 반복한다.
        if self.missileStart() and self.launchStart():
            if self.patternCheck:  # 발사 한번에 랜덤 패턴값 하나
                self.randomPattern = random.choice(self.missilePattern)  # 패턴중 하나를 골라 변수에 저장
                self.patternCheck = False  # 한가지 패턴으로 4초간 발사

            # 미사일 발사간격 = 0.2초 간격으로 발사
            # launchStart가 열려있는 동안 missileInterval 함수 계속 호출
            if self.missileInterval():
                if self.randomPattern == '1':
                    bossMissiles.add(
                        bossMissile_moving(randomX, self.centerY + 40, self.randomPattern, self.missileType))
                self.intervalStartTime = time.time()

    # 첫 발사
    def missileStart(self):
        endTime = time.time()
        resultTime = endTime - self.startTime

        if resultTime >= 11:  # 등장하고 11초가 지나면 발사 시작
            return True
        else:
            return False

    # 미사일 발사 지속시간
    def launchStart(self):
        # 미사일 발사 시간 측정 변수
        # 4초간 발사하고 3초간 쿨타임
        endTime = time.time()
        resultTime = endTime - self.MissileStartTime
        if resultTime <= self.launchTime:
            return True

        # 3초 쿨타임
        else:
            if resultTime >= self.launchTime + 3:
                self.MissileStartTime = time.time()
                self.patternCheck = True  # 패턴 재설정

            return False

    # 미사일 발사 간격
    def missileInterval(self):
        endTime = time.time()
        resultTime = endTime - self.intervalStartTime

        if resultTime >= 0.2:  # 0.2초 간격으로 발사
            return True
        else:
            return False

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_mask(self, sprite):
                return sprite

# BossMissile Class
class BossMissile(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, pattern, type):
        super(BossMissile, self).__init__()
        self.image = pygame.image.load(images + 'boss_missile0' + type + '.png')
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.pattern = pattern

    def update(self):
        # 1: 직선이동
        if self.pattern == '1':
            self.rect.y += 2
            # UFO 미사일이 화면 끝까지가면 삭제
            if self.out():
                self.kill()

    def out(self):
        if self.rect.y > gameHeight:
            return True


# 이벤트1 - 전기 이벤트
class Electricity(pygame.sprite.Sprite):
    def __init__(self, speed):
        super(Electricity, self).__init__()
        self.image = pygame.image.load(images + 'electric.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = -300
        self.speed = speed

    def update(self):
        global changeDir
        if changeDir == False:
            self.rect.y += self.speed
            if self.rect.y > gameHeight * 0.8:
                changeDir = True  # 진행방향을 바꾼다

        elif changeDir == True:
            self.rect.y -= self.speed

    def out(self):
        if changeDir == True and self.rect.y < -40:
            return True

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_mask(self, sprite):
                return sprite


# ufo class update 관련 함수
def ufo_moving(xpos, ypos, xspeed, yspeed, missileType, missilePattern, ufoMissileSpeed, ufoMissileStartTime):
    return UFO(xpos, ypos, xspeed, yspeed, missileType, missilePattern, ufoMissileSpeed, ufoMissileStartTime)


# missile class update 관련 함수
def missile_moving(xpos, ypos, speed):
    global spaceshipCount
    return Missile(spaceshipCount, xpos, ypos, speed)


# UFO Missile class update 관련 함수
def ufoMissile_moving(xpos, ypos, missileType, missilePattern, ufoMissileSpeed, ufoMissileStartTime):
    return UFOMissile(xpos, ypos, missileType, missilePattern, ufoMissileSpeed, ufoMissileStartTime)


# Nuclear class update 관련 함수
def nuclear_launch():
    return Nuclear()


# Boss class update 관련 함수
def bossMissile_moving(xpos, ypos, pattern, type):
    return BossMissile(xpos, ypos, pattern, type)


# 텍스트 출력 함수
def draw_text(text, font, surface, xpos, ypos, color):  # (출력할 텍스트, 폰트, 스크린, 출력위치, 색상)
    text_obj = font.render(text, True, color)  # (출력할 텍스트, 안티앨리어싱, 컬러)
    text_rect = text_obj.get_rect()
    text_rect.centerx = xpos
    text_rect.centery = ypos
    surface.blit(text_obj, text_rect)


def run():
    global screen, FPS, spaceshipLevel, spaceshipCount, roundLevel, roundCount, missileCount, roundTime, respawnTime, money, score, changeDir, \
        life, nuclearCount

    roundCount = str(roundLevel)
    spaceshipCount = str(spaceshipLevel)

    backgroundMusic.play()  # 배경음악 재생

    systemOn = True
    moneyImage = False  # player 돈 얻는 이미지
    hitImage = False  # player 히트 이미지

    boss_spawn = False  # 보스 출현 변수
    boss_kill = False  # 보스 킬 체크
    bossExplosionImage = False  # boss 폭발 이미지

    spaceshipCount = str(spaceshipLevel)
    background = pygame.image.load(images + 'background_level' + roundCount + '.png')

    player = Player(spaceshipCount)  # player 객체 생성
    player.set_pos(gameWidth * 0.5, gameHeight * 0.9)  # spaceship 초기 위치 지정

    # 전기 이벤트 초기화
    electricity = Electricity(roundLevel)
    elec_prob = False  # 전기 이벤트 발생 체크
    elec_spawn = True  # 이벤트가 한번만 발생되도록 하는 변수
    warningSoundCheck = True  # 소리를 한번만 출력하도록 하는 변수

    # player 이동 값 저장 변수 (x, y: player의 현재 위치, spaceshipX, spaceshipY: 이동한 좌표 값)
    x = player.rect.x + player.centerX
    y = player.rect.y + player.centerY
    spaceshipX = 0
    spaceshipY = 0

    roundStartTime = time.time()  # 라운드 시간 측정
    respawnStartTime = time.time()  # ufo 리스폰 시간 측정
    missileStartTime = time.time()  # missile 카운트 시간 측정

    while systemOn:
        pygame.display.update()
        clock.tick(FPS)  # fps 설정

        screen.blit(background, (0, 0))  # 백그라운드 이미지 로드
        screen.blit(moneyBag, (410, 720))  # 돈주머니 이미지 로드
        screen.blit(lifeImage, (10, 755))  # 생명 이미지 로드
        screen.blit(nuclearMissileImage, (340, 720))  # 핵미사일 이미지 로드

        # 텍스트 로드 (텍스트, 폰트, 출력화면, x좌표, y좌표, 색상)
        draw_text('RouND: {}'.format(roundLevel), gameFont24, screen, 75, 10, WHITE)  # score 텍스트-
        draw_text('SCoRE: {}'.format(score), gameFont24, screen, 370, 10, WHITE)  # score 텍스트
        draw_text(format(money), numberFont16, screen, 440, 790, WHITE)  # money 텍스트
        draw_text(format(life), gameFont24, screen, 75, 770, RED)  # 생명 텍스트
        draw_text(format(nuclearCount), numberFont16, screen, 360, 790, WHITE)  # 핵미사일 개수 텍스트

        screen.blit(player.image, player.rect)  # player 이미지 로드

        # ufo 자동생성을 위한 시간 측정 변수
        # 라운드 시간 측정 변수
        roundEndTime = time.time()
        roundResultTime = roundEndTime - roundStartTime
        # 리스폰 시간 측정 변수
        respawnEndTime = time.time()
        respawnResultTime = respawnEndTime - respawnStartTime

        if roundResultTime <= roundTime:  # roundTime 까지 ufo 자동생성
            for i in range(random.randint(roundLevel, roundLevel + 3)):
                if respawnResultTime >= respawnTime:  # respawnTime 기다리기
                    flag = random.choice(direction)  # 'Down', 'Right', 'Left' 중 하나를 임의로 선택
                    randomX = random.randint(0, gameWidth * 0.8)  # 초기 등장 X좌표
                    randomY = random.randint(0, gameHeight * 0.3)  # 초기 등장 Y좌표
                    randomPattern = random.choice(pattern)  # '1', '2', '3', '4' 중 하나를 임의로 선택

                    if (flag == 'Down'):
                        # x좌표, y좌표, x스피드, y스피드, 미사일 타입, 미사일 패턴, 미사일 속도, startTime
                        ufos.add(ufo_moving(randomX, 0, 0, 1, roundCount, randomPattern, 3, time.time()))
                        respawnStartTime = time.time()  # 생성 후 타이머 재시작
                    elif (flag == 'Right'):
                        ufos.add(ufo_moving(0, randomY, 1, 0, roundCount, randomPattern, 3, time.time()))
                        respawnStartTime = time.time()
                    elif (flag == 'Left'):
                        ufos.add(ufo_moving(gameWidth, randomY, -1, 0, roundCount, randomPattern, 3, time.time()))
                        respawnStartTime = time.time()

                else:
                    continue  # 시간 채워질때까지 반복 건너뛰기

        # roundTime 지나면 보스 출현
        if boss_spawn == False and roundResultTime >= roundTime + 5:
            boss_spawn = True
            boss = Boss(roundCount)
            warning.play()  # 등장 소리 출력

        # 보스출현 #
        if boss_spawn:
            boss.update()
            screen.blit(boss.image, boss.rect)
            bossMissiles.update()
            bossMissiles.draw(screen)

            # player와 boss 충돌 시
            if pygame.sprite.collide_mask(player, boss):
                screen.blit(playerExplosion, player.rect)
                pygame.display.update()
                playerExplosionSound.play()  # 플레이어 폭발 사운드 재생
                pygame.mixer.music.stop()  # 배경음악 재생 중지
                time.sleep(2)
                ufos.empty()
                ufoMissiles.empty()
                bossMissiles.empty()
                score = 0
                money = 0
                missileCount = 0
                gameOver()

            # Player - Boss 미사일 충돌 판단
            if pygame.sprite.spritecollide(player, bossMissiles, True, pygame.sprite.collide_circle_ratio(0.675)):
                life -= random.randint(10, roundLevel * 10)
                playerHitSound.play()  # 소리 출력
                hitLoadStartTime = time.time()
                hitImage = True  # hit 이미지 출력 시작

                # 생명이 다 떨어지면 player 우주선 폭파
                if life <= 0:
                    screen.blit(playerExplosion, player.rect)
                    pygame.display.update()
                    backgroundMusic.stop()  # 배경음악 재생 중지
                    playerExplosionSound.play()  # 플레이어 폭발 사운드 재생
                    time.sleep(2)
                    life = 100
                    gameOver()

            # Player 미사일 - Boss 충돌 판단
            if pygame.sprite.spritecollide(boss, playerMissiles, True):
                boss.life -= spaceshipLevel * 2
                playerHitSound.play()  # 소리 출력

            # 보스가 죽으면
            if boss_kill == False and boss.life <= 0:
                boss_kill = True
                imageStartTime = time.time()
                bossExplosionImage = True

            # 애니메이션 기능 #
            if bossExplosionImage:
                bossMissiles.empty()

                imageEndTime = time.time()
                imageResultTime = imageEndTime - imageStartTime

                if imageResultTime <= imageTime:
                    playerExplosionSound.play()
                    screen.blit(bossExplosion01, (boss.rect.x, boss.rect.y))
                    pygame.display.update()

                elif imageResultTime > imageTime and imageResultTime <= imageTime * 2:
                    screen.blit(bossExplosion01, (boss.rect.x + 80, boss.rect.y - 40))
                    pygame.display.update()

                elif imageResultTime > imageTime * 2 and imageResultTime <= imageTime * 3:
                    screen.blit(bossExplosion01, (boss.rect.x + 160, boss.rect.y))
                    pygame.display.update()

                elif imageResultTime > imageTime * 3 and imageResultTime <= imageTime * 4:
                    screen.blit(bossExplosion01, (boss.rect.x + 240, boss.rect.y - 40))
                    pygame.display.update()

                elif imageResultTime > imageTime * 4 and imageResultTime <= imageTime * 8:
                    nuclearExplosionSound.play()
                    screen.blit(bossExplosion02, (boss.rect.x, boss.rect.y - 70))
                    pygame.display.update()

                # 이미지 출력이 다 끝나면 아래문장 실행
                else:
                    bossExplosionImage = False  # 이미지 출력 중지
                    # 다음 라운드 진행
                    backgroundMusic.stop()
                    coinSound.play()  # 돈 얻는 소리 출력
                    screen.blit(moneyUp, (x, y))
                    pygame.display.update()
                    money += 300  # 보스를 클리어하면 300원을 얻는다.
                    ufos.empty()
                    ufoMissiles.empty()
                    playerMissiles.empty()
                    player.kill()
                    # 라운드 통과 메세지, 소리
                    if roundLevel < 4:  # 최종 라운드는 4라운드
                        roundLevel += 1
                        time.sleep(4)
                        backgroundMusic.stop()
                        station()

                    else:  # 최종 라운드가 끝나면 게임이 종료된다.
                        time.sleep(2)
                        backgroundMusic.stop()
                        gameEnd()  # 게임 종료화면으로 돌아가기

        ''' Electricity 이벤트 발동 조건 - 라운드 중 단 한번만 발동하게 하기
            while 문 밖 elec_prob(등장 확률) 은 False, elec_spawn(등장 Check 변수)은 True로 둔다.
            아래 if 문에서 확률 조건이 만족하면 elec_prob을 True로 바꾸고 이벤트를 등장시킨다.
            전기 이벤트가 화면 밖으로 벗어나면 해당 오브젝트 삭제 후 elec_prob과 elec_spawn 모두 닫아
            재 등장 하지 않게 한다. '''

        # 등장확률: 초당 1/roundTime 확률, 보스가 나왔을땐 실행하지 않는다.
        if boss_spawn == False and elec_spawn and random.randint(1, roundTime * FPS) == 1:
            elec_prob = True
            if warningSoundCheck:
                warning.play()  # 등장 소리 출력
                warningSoundCheck = False

        if elec_prob:
            electricity.update()
            screen.blit(electricity.image, electricity.rect)
            if electricity.out():
                electricity.kill()
                changeDir = False  # changeDir 변수 초기화
                elec_prob = False
                elec_spawn = False

        ufos.update()
        ufos.draw(screen)
        ufoMissiles.update()
        ufoMissiles.draw(screen)

        # 버튼 입력으로 제어하기
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # left
                if event.key == pygame.K_a:
                    print("================================================================================")
                    spaceshipX -= 2.0

                # right
                if event.key == pygame.K_d:
                    spaceshipX += 2.0

                # up
                if event.key == pygame.K_w:
                    spaceshipY -= 2.0

                # down
                if event.key == pygame.K_s:
                    spaceshipY += 2.0

                # 미사일
                if event.key == pygame.K_SPACE:
                    if missileCount != 0:  # missileCount 초기값 = 0
                        shootingSound.play()  # 발사 소리 출력
                        # 현재 player의 x좌표, y좌표, 미사일 속도
                        playerMissiles.add(missile_moving(x, y * 0.89, missileSpeed))
                        missileCount -= 1

                    # 발사 불가능(재장전)
                    elif missileCount == 0:
                        # 미사일 재장전 시간 측정 변수
                        missileEndTime = time.time()
                        missileResultTime = missileEndTime - missileStartTime
                        # 설정한 시간동안 대기
                        if missileResultTime >= reloadTime:  # reloadTime이 지나면 발사 가능 (missileCount = 0)
                            missileCount = 1  # 레벨 비례 미사일 충전
                            missileStartTime = time.time()  # 타이머 재시작

                # 핵미사일
                if event.key == pygame.K_k:
                    # 핵미사일 발사
                    if nuclearCount > 0:
                        nuclear.add(nuclear_launch())
                        nuclearCount -= 1

            # 키보드 입력 중지 이벤트
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    spaceshipX = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    spaceshipY = 0

        # spaceship 좌표조정
        x += spaceshipX
        y += spaceshipY
        print("X: " + str(spaceshipX))
        print("Y: " + str(spaceshipY))


        # 우주선이 화면 밖으로 못나가도록
        if x <= 0 + player.centerX:
            x = 0 + player.centerX

        if x >= gameWidth - player.centerX:
            x = gameWidth - player.centerX

        if y <= 0 + player.centerY:
            y = 0 + player.centerY

        if y >= gameHeight - player.centerY:
            y = gameHeight - player.centerY

        # 우주선 좌표 업데이트
        player.set_pos(x, y)

        # player missile 좌표 업데이트
        playerMissiles.update()
        playerMissiles.draw(screen)

        # Nuclear 업데이트
        nuclear.update()
        nuclear.draw(screen)

        # Player - UFO 충돌 판단
        if player.collide(ufos):
            screen.blit(playerExplosion, player.rect)
            pygame.display.update()
            backgroundMusic.stop()  # 배경음악 재생 중지
            playerExplosionSound.play()  # 플레이어 폭발 사운드 재생
            time.sleep(2)
            life = 100
            gameOver()

        # Missile - UFO 충돌 판단
        if pygame.sprite.groupcollide(ufos, playerMissiles, True, True):
            ufoExplosionSound.play()  # ufo 폭발 효과음 재생
            score += random.randint(roundLevel * 111, roundLevel * 122)  # 스코어 증가
            if random.randint(1, getMoney) == 1:  # 확률 1/getMoney
                money += roundLevel * 100  # 돈 증가
                coinSound.play()  # 돈 얻는 소리 출력
                moneyLoadStartTime = time.time()  # 이미지 출력 시간 측정
                moneyImage = True  # 돈 얻는 이미지 출력 시작

        # 돈 얻는 이미지 출력
        if moneyImage:
            moneyLoadEndTime = time.time()
            moneyLoadResultTime = moneyLoadEndTime - moneyLoadStartTime
            if moneyLoadResultTime <= moneyLoadTime:
                screen.blit(moneyUp, (x, y))
                pygame.display.update()

            else:
                moneyLoadStartTime = time.time()
                moneyImage = False  # 이미지 출력 중지

        # Player - UFO미사일 충돌
        if pygame.sprite.spritecollide(player, ufoMissiles, True, pygame.sprite.collide_circle_ratio(0.675)):
            life -= random.randint(roundLevel * 3, roundLevel * 4)
            playerHitSound.play()  # 소리 출력
            hitLoadStartTime = time.time()
            hitImage = True  # hit 이미지 출력 시작

            # 생명이 다 떨어지면 player 우주선 폭파
            if life <= 0:
                screen.blit(playerExplosion, player.rect)
                pygame.display.update()
                backgroundMusic.stop()  # 배경음악 재생 중지
                playerExplosionSound.play()  # 플레이어 폭발 사운드 재생
                time.sleep(2)
                life = 100
                gameOver()

        # hit 이미지 출력
        if hitImage:
            hitLoadEndTime = time.time()
            hitLoadResultTime = hitLoadEndTime - hitLoadStartTime
            if hitLoadResultTime <= hitLoadTime:
                screen.blit(playerHit, (x, y))
                pygame.display.update()

            else:
                hitLoadStartTime = time.time()
                hitImage = False  # 이미지 출력 중지

        # 전기 이벤트와 player 충돌 시
        if pygame.sprite.collide_mask(player, electricity):
            screen.blit(playerExplosion, player.rect)
            pygame.display.update()
            backgroundMusic.stop()  # 배경음악 재생 중지
            playerExplosionSound.play()  # 플레이어 폭발 사운드 재생
            time.sleep(2)
            gameOver()


# 게임 시작화면
def gameStart():
    global buttonState, roundLevel, spaceshipLevel, life, missileCount

    roundLevel = 1
    spaceshipLevel = 1
    life = 100
    missileCount = 0

    background = pygame.image.load(images + 'game_start.png')
    startBackgroundMusic.play()  # 배경음악 출력

    while True:
        screen.blit(background, (0, 0))
        pygame.display.update()

        # 아무키나 입력 받음
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                clickSound.play()
                gameEx()  # 게임 설명 화면으로

# 게임 설명
def gameEx():
    global buttonState

    background = pygame.image.load(images + 'game_ex.png')

    while True:
        screen.blit(background, (0, 0))
        pygame.display.update()

        # 1초 후에 버튼 입력 받음 - 이전 화면에서 눌렸던 버튼이 여기까지 영향가는 것을 방지
        # 아무키나 입력 받음
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                startBackgroundMusic.stop()
                clickSound.play()
                run()  # 게임 시작

# 우주 정거장
def station():
    global buttonState, spaceshipLevel, spaceshipCount, life, nuclearCount, money

    backgroundMusic.stop()
    stationSound.play()

    selectNum = 1  # 1번은 첫번째 2번 두번째 3번 세번째

    while True:
        pygame.display.update()
        selectCount = str(selectNum)
        stationImage = pygame.image.load(images + 'station' + spaceshipCount + selectCount + '.jpg')
        screen.blit(stationImage, (0, 0))
        draw_text(format(money), numberFont20, screen, 80, 765, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    if selectNum < 3:
                        selectNum += 1
                        clickSound2.play()
                    else:
                        pass

                if event.key == pygame.K_a:
                    if selectNum > 1:
                        selectNum -= 1
                        clickSound2.play()
                    else:
                        pass

                if event.key == pygame.K_SPACE:
                    # 비행기 업그레이드
                    if selectNum == 1 and money >= 500 and spaceshipLevel < 4:
                        money -= 500
                        spaceshipLevel += 1
                        spaceshipCount = str(spaceshipLevel)
                        buySound.play()

                    # 생명 회복
                    elif life != 100 and selectNum == 2 and money >= 100:
                        money -= 100
                        life = 100
                        buySound.play()

                    # 핵미사일 구매
                    elif selectNum == 3 and money >= 100 and nuclearCount < 1:  # 핵미사일 최대 개수 1개
                        money -= 100
                        nuclearCount += 1
                        buySound.play()

                    else:
                        errorSound.play()

                if event.key == pygame.K_ESCAPE:
                    # 게임 시작으로 넘어 가기 위해 메시지창을 띄운다
                    while True:
                        question_image = pygame.image.load(images + 'question.jpg')
                        screen.blit(question_image, (0, 0))
                        pygame.display.update()
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                stationSound.stop()
                                run()

def gameOver():
    global buttonState, score, money, missileCount

    bossMissiles.empty()
    ufos.empty()
    ufoMissiles.empty()
    score = 0
    money = 0
    missileCount = 0

    gameOverImage = pygame.image.load(images + 'gameover.png')  # 게임 오버 이미지

    while True:
        screen.blit(gameOverImage, (0, 0))
        pygame.display.update()
        # 아무키나 입력 받음
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                gameStart()  # 초기 화면으로 돌아가기

def gameEnd():
    global buttonState, score, money, missileCount

    backgroundMusic = pygame.mixer.Sound(background + 'Game_Over.wav')
    backgroundMusic.play()

    bossMissiles.empty()
    ufos.empty()
    ufoMissiles.empty()
    score = 0
    money = 0
    missileCount = 0

    gameEndImg = pygame.image.load(images + 'game_ending.png')  # 게임 엔딩 이미지

    while True:
        screen.blit(gameEndImg, (0, 0))
        pygame.display.update()
        # 아무키나 입력 받음

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                gameStart()  # 초기 화면으로 돌아가기


# END#
gameStart()

