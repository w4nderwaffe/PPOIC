#include "RubikCube.hpp"
#include <fstream>
#include <random>
#include <ctime>
#include <cmath>

// ===== helpers (поворот локальных осей) =====
int RubikCube::rotMapAxis(int v, char axis, bool cw) {
    int s = v > 0 ? 1 : -1;
    int a = std::abs(v);
    if (axis == 'X' && a != 1) {
        if (cw) { if (a==2) return  s*3; if (a==3) return -s*2; }
        else    { if (a==2) return -s*3; if (a==3) return  s*2; }
    }
    if (axis == 'Y' && a != 2) {
        if (cw) { if (a==1) return -s*3; if (a==3) return  s*1; }
        else    { if (a==1) return  s*3; if (a==3) return -s*1; }
    }
    if (axis == 'Z' && a != 3) {
        if (cw) { if (a==1) return  s*2; if (a==2) return -s*1; }
        else    { if (a==1) return -s*2; if (a==2) return  s*1; }
    }
    return v;
}

void RubikCube::rotateOrientation(Cubelet& c, char axis, bool cw) {
    c.ax = rotMapAxis(c.ax, axis, cw);
    c.ay = rotMapAxis(c.ay, axis, cw);
    c.az = rotMapAxis(c.az, axis, cw);
}

// ===== конструктор и инициализация =====
RubikCube::RubikCube() { initSolved(); }

void RubikCube::initSolved() {
    for(int x=0;x<3;x++)
        for(int y=0;y<3;y++)
            for(int z=0;z<3;z++)
                cubie_[x][y][z] = { x,y,z, +1,+2,+3 };
}

void RubikCube::initRandom(int turns) {
    static std::mt19937 rng{std::random_device{}()};
    const char faces[6]={'U','D','L','R','F','B'};
    std::uniform_int_distribution<int> df(0,5), dd(0,1);
    for(int i=0;i<turns;i++) startRotation(faces[df(rng)], dd(rng)!=0); // через очередь
}

// ===== файл =====
bool RubikCube::loadFromFile(const std::string& path) {
    std::ifstream in(path);
    if(!in) return false;
    for(int x=0;x<3;x++)
        for(int y=0;y<3;y++)
            for(int z=0;z<3;z++) {
                Cubelet c{};
                if(!(in >> c.homeX >> c.homeY >> c.homeZ >> c.ax >> c.ay >> c.az)) return false;
                cubie_[x][y][z]=c;
            }
    return true;
}
bool RubikCube::saveToFile(const std::string& path) const {
    std::ofstream out(path);
    if(!out) return false;
    for(int x=0;x<3;x++)
        for(int y=0;y<3;y++)
            for(int z=0;z<3;z++) {
                const auto& c=cubie_[x][y][z];
                out<<c.homeX<<" "<<c.homeY<<" "<<c.homeZ<<" "<<c.ax<<" "<<c.ay<<" "<<c.az<<"\n";
            }
    return true;
}

// ===== логика поворота слоя (моментальная фиксация) =====
void RubikCube::rotateFace(char face, bool clockwise) {
    int layer=0; char axis=' ';
    switch(face) {
        case 'U': layer=2; axis='Y'; break;
        case 'D': layer=0; axis='Y'; clockwise=!clockwise; break; // смотрим снизу
        case 'L': layer=0; axis='X'; clockwise=!clockwise; break; // смотрим слева
        case 'R': layer=2; axis='X'; break;
        case 'F': layer=2; axis='Z'; break;
        case 'B': layer=0; axis='Z'; clockwise=!clockwise; break; // смотрим сзади
        default: return;
    }

    Cubelet tmp[3][3][3];
    for(int x=0;x<3;x++) for(int y=0;y<3;y++) for(int z=0;z<3;z++) tmp[x][y][z]=cubie_[x][y][z];

    auto rot=[&](int a,int b){ return clockwise ? std::pair<int,int>(b,2-a) : std::pair<int,int>(2-b,a); };

    if(axis=='X'){
        int x=layer;
        for(int y=0;y<3;y++)for(int z=0;z<3;z++){
            auto [ny,nz]=rot(y,z);
            cubie_[x][ny][nz]=tmp[x][y][z];
            rotateOrientation(cubie_[x][ny][nz],axis,clockwise);
        }
    } else if(axis=='Y'){
        int y=layer;
        for(int x=0;x<3;x++)for(int z=0;z<3;z++){
            auto [nx,nz]=rot(x,z);
            cubie_[nx][y][nz]=tmp[x][y][z];
            rotateOrientation(cubie_[nx][y][nz],axis,clockwise);
        }
    } else { // Z
        int z=layer;
        for(int x=0;x<3;x++)for(int y=0;y<3;y++){
            auto [nx,ny]=rot(x,y);
            cubie_[nx][ny][z]=tmp[x][y][z];
            rotateOrientation(cubie_[nx][ny][z],axis,clockwise);
        }
    }
}

bool RubikCube::isSolved() const {
    for(int x=0;x<3;x++)
        for(int y=0;y<3;y++)
            for(int z=0;z<3;z++) {
                const auto& c=cubie_[x][y][z];
                if (c.homeX!=x || c.homeY!=y || c.homeZ!=z || c.ax!=+1 || c.ay!=+2 || c.az!=+3)
                    return false;
            }
    return true;
}

// ===== анимация =====
void RubikCube::startRotation(char face, bool cw){
    if(current_.active) queue_.push_back({face,cw,0.f,false});
    else                current_={face,cw,0.f,true};
}
void RubikCube::updateRotation(float dt){
    if(!current_.active) return;
    const float speedDegPerSec = 360.f; // 90° за 0.25 с
    current_.progress += speedDegPerSec * dt;
    if(current_.progress >= 90.f){
        current_.progress = 90.f;
        rotateFace(current_.face, current_.clockwise); // зафиксировать модель
        current_.active = false;
        if(!queue_.empty()){ current_ = queue_.front(); queue_.erase(queue_.begin()); current_.active=true; current_.progress=0.f; }
    }
}
bool RubikCube::isInLayer(int i,int j,int k, char face){
    if(face=='U') return j==2;
    if(face=='D') return j==0;
    if(face=='L') return i==0;
    if(face=='R') return i==2;
    if(face=='F') return k==2;
    if(face=='B') return k==0;
    return false;
}
char RubikCube::faceAxis(char face){
    if(face=='U' || face=='D') return 'Y';
    if(face=='L' || face=='R') return 'X';
    return 'Z';
}
int RubikCube::faceLayer(char face){
    if(face=='U' || face=='R' || face=='F') return 2;
    return 0;
}

// ===== управление/события =====
void RubikCube::handleEvent(const sf::Event& event) {
    if (event.type==sf::Event::KeyPressed) {
        bool shift = sf::Keyboard::isKeyPressed(sf::Keyboard::LShift) ||
                     sf::Keyboard::isKeyPressed(sf::Keyboard::RShift);
        bool cw=!shift;
        if(event.key.code==sf::Keyboard::U) startRotation('U',cw);
        if(event.key.code==sf::Keyboard::D) startRotation('D',cw);
        if(event.key.code==sf::Keyboard::L) startRotation('L',cw);
        if(event.key.code==sf::Keyboard::R) startRotation('R',cw);
        if(event.key.code==sf::Keyboard::F) startRotation('F',cw);
        if(event.key.code==sf::Keyboard::B) startRotation('B',cw);

        if(event.key.code==sf::Keyboard::Left)  angleY_-=5.f;
        if(event.key.code==sf::Keyboard::Right) angleY_+=5.f;
        if(event.key.code==sf::Keyboard::Up)    angleX_-=5.f;
        if(event.key.code==sf::Keyboard::Down)  angleX_+=5.f;
    }
    if (event.type==sf::Event::MouseButtonPressed && event.mouseButton.button==sf::Mouse::Left){
        dragging_=true; lastMouseX_=event.mouseButton.x; lastMouseY_=event.mouseButton.y;
    }
    if (event.type==sf::Event::MouseButtonReleased && event.mouseButton.button==sf::Mouse::Left){
        dragging_=false;
    }
    if (event.type==sf::Event::MouseMoved && dragging_){
        int dx=event.mouseMove.x-lastMouseX_;
        int dy=event.mouseMove.y-lastMouseY_;
        angleY_+=dx*0.5f; angleX_+=dy*0.5f;
        lastMouseX_=event.mouseMove.x; lastMouseY_=event.mouseMove.y;
    }
    if (event.type==sf::Event::MouseWheelScrolled){
        distZ_ += -event.mouseWheelScroll.delta;
        if(distZ_>-4.f)  distZ_=-4.f;
        if(distZ_<-30.f) distZ_=-30.f;
    }
}

void RubikCube::update() {
    float dt = clock_.restart().asSeconds();
    updateRotation(dt);
}

// ===== рендер =====
void RubikCube::setupProjection_(int width,int height){
    float aspect=(height==0)?1.f:(float)width/(float)height;
    float fovy=60.f;
    float zNear=0.1f,zFar=100.f;
    float f=1.0f/std::tan(fovy*0.5f*3.14159f/180.f);

    GLfloat proj[16]={
        f/aspect,0,0,0,
        0,f,0,0,
        0,0,(zFar+zNear)/(zNear-zFar),-1,
        0,0,(2*zFar*zNear)/(zNear-zFar),0
    };

    glMatrixMode(GL_PROJECTION);
    glLoadMatrixf(proj);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
}

void RubikCube::colorForWorldDir(const Cubelet& c, int dir, float& r,float& g,float& b){
    auto set=[&](float R,float G,float B){ r=R; g=G; b=B; };
    if      ( c.ax == dir) { set(0.85f,0.20f,0.20f); return; } // +X red
    else if (-c.ax == dir) { set(0.95f,0.55f,0.15f); return; } // -X orange
    else if ( c.ay == dir) { set(0.95f,0.95f,0.95f); return; } // +Y white
    else if (-c.ay == dir) { set(0.95f,0.90f,0.20f); return; } // -Y yellow
    else if ( c.az == dir) { set(0.20f,0.85f,0.20f); return; } // +Z green
    else                   { set(0.20f,0.35f,0.95f); return; } // -Z blue
}

void RubikCube::drawCubelet_(const Cubelet& c,float cx,float cy,float cz,float size,
                             int i,int j,int k){
    const float s=size*0.5f;
    glPushMatrix();
    glTranslatef(cx,cy,cz);

    auto drawQuad = [](float x0,float y0,float z0,
                       float x1,float y1,float z1,
                       float x2,float y2,float z2,
                       float x3,float y3,float z3){
        glBegin(GL_TRIANGLES);
        glVertex3f(x0,y0,z0); glVertex3f(x1,y1,z1); glVertex3f(x2,y2,z2);
        glVertex3f(x0,y0,z0); glVertex3f(x2,y2,z2); glVertex3f(x3,y3,z3);
        glEnd();
    };

    // 1) Чёрный корпус (с polygon offset, чтобы не затирал наклейки)
    glEnable(GL_POLYGON_OFFSET_FILL);
    glPolygonOffset(1.0f, 1.0f);
    glColor3f(0.f,0.f,0.f);
    drawQuad( s,-s,-s,  s, s,-s,  s, s, s,  s,-s, s); // +X
    drawQuad(-s,-s, s, -s, s, s, -s, s,-s, -s,-s,-s); // -X
    drawQuad(-s, s,-s,  s, s,-s,  s, s, s, -s, s, s); // +Y
    drawQuad(-s,-s, s,  s,-s, s,  s,-s,-s, -s,-s,-s); // -Y
    drawQuad(-s,-s, s, -s, s, s,  s, s, s,  s,-s, s); // +Z
    drawQuad( s,-s,-s,  s, s,-s, -s, s,-s, -s,-s,-s); // -Z
    glDisable(GL_POLYGON_OFFSET_FILL);

    // 2) Наклейки (только наружные стороны)
    auto face = [&](int dir){
        float r,g,b; colorForWorldDir(c, dir, r,g,b);
        glColor3f(r,g,b);
        switch(dir){
            case +1: if(i==2) drawQuad( s,-s,-s,  s, s,-s,  s, s, s,  s,-s, s); break;
            case -1: if(i==0) drawQuad(-s,-s, s, -s, s, s, -s, s,-s, -s,-s,-s); break;
            case +2: if(j==2) drawQuad(-s, s,-s,  s, s,-s,  s, s, s, -s, s, s); break;
            case -2: if(j==0) drawQuad(-s,-s, s,  s,-s, s,  s,-s,-s, -s,-s,-s); break;
            case +3: if(k==2) drawQuad(-s,-s, s, -s, s, s,  s, s, s,  s,-s, s); break;
            case -3: if(k==0) drawQuad( s,-s,-s,  s, s,-s, -s, s,-s, -s,-s,-s); break;
        }
    };

    face(+1); face(-1); face(+2); face(-2); face(+3); face(-3);

    glPopMatrix();
}

void RubikCube::render(int width,int height){
    setupProjection_(width,height);
    glTranslatef(0.f,0.f,distZ_);
    glRotatef(angleX_,1.f,0.f,0.f);
    glRotatef(angleY_,0.f,1.f,0.f);

    const float spacing=1.05f; // зазор между кублетами
    const float size=0.95f;    // сами кубики чуть меньше
    const float start=-spacing;

    // Параметры текущей анимации
    char animAxis = 0;
    int  animLayer = -1;
    float animAngle = 0.f;
    if(current_.active){
        animAxis  = faceAxis(current_.face);
        animLayer = faceLayer(current_.face);

        // <<< ВАЖНО: знак угла для D/L/B инвертирован, как и в rotateFace >>>
        const float faceSign = (current_.face=='U' || current_.face=='R' || current_.face=='F') ? +1.f : -1.f;
        animAngle = current_.progress * (current_.clockwise ? +1.f : -1.f) * faceSign;
    }

    for(int i=0;i<3;i++){
        for(int j=0;j<3;j++){
            for(int k=0;k<3;k++){
                const Cubelet &c = cubie_[i][j][k];
                glPushMatrix();

                float px = start + i*spacing;
                float py = start + j*spacing;
                float pz = start + k*spacing;

                if(current_.active && isInLayer(i,j,k,current_.face)){
                    // центр текущего слоя
                    float cx = (animAxis=='X') ? (start + animLayer*spacing) : 0.f;
                    float cy = (animAxis=='Y') ? (start + animLayer*spacing) : 0.f;
                    float cz = (animAxis=='Z') ? (start + animLayer*spacing) : 0.f;

                    glTranslatef(cx, cy, cz);
                    if(animAxis=='X') glRotatef(animAngle, 1.f,0.f,0.f);
                    if(animAxis=='Y') glRotatef(animAngle, 0.f,1.f,0.f);
                    if(animAxis=='Z') glRotatef(animAngle, 0.f,0.f,1.f);
                    glTranslatef(px - cx, py - cy, pz - cz);
                } else {
                    glTranslatef(px, py, pz);
                }

                drawCubelet_(c, 0.f,0.f,0.f, size, i,j,k);
                glPopMatrix();
            }
        }
    }
}

// ===== ТЕСТОВЫЕ УТИЛИТЫ =====
std::string RubikCube::serialize() const {
    std::string s;
    s.reserve(27*6*3);
    for(int x=0;x<3;x++)
        for(int y=0;y<3;y++)
            for(int z=0;z<3;z++) {
                const auto& c = cubie_[x][y][z];
                s.append(std::to_string(c.homeX)).push_back(',');
                s.append(std::to_string(c.homeY)).push_back(',');
                s.append(std::to_string(c.homeZ)).push_back(',');
                s.append(std::to_string(c.ax)).push_back(',');
                s.append(std::to_string(c.ay)).push_back(',');
                s.append(std::to_string(c.az)).push_back(';');
            }
    return s;
}
std::uint64_t RubikCube::stateHash() const {
    // простой 64-битный FNV-1a по сериализации
    const std::string data = serialize();
    std::uint64_t h = 1469598103934665603ull;
    for (unsigned char c : data) {
        h ^= c;
        h *= 1099511628211ull;
    }
    return h;
}
