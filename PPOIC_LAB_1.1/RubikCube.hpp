#pragma once
#include <SFML/Window.hpp>
#include <SFML/OpenGL.hpp>
#include <array>
#include <string>
#include <vector>
#include <cstdint>

// Макрос для тестирования - в продакшене пустой
#ifdef TESTING
#define TESTABLE public
#else
#define TESTABLE private
#endif

// Логический кублет: "дом" + ориентация локальных осей (±1=X, ±2=Y, ±3=Z)
struct Cubelet {
    int homeX, homeY, homeZ;  // позиция в решённом виде
    int ax, ay, az;           // ориентация локальных осей в мировых
};

class RubikCube {
public:
    RubikCube();

    // Инициализация
    void initSolved();
    void initRandom(int turns = 25);

    // Файл
    bool loadFromFile(const std::string& path);
    bool saveToFile(const std::string& path) const;

    // Логика (моментальный поворот модели — используется по завершении анимации)
    // face: 'U','D','L','R','F','B', clockwise — по часовой при взгляде на грань снаружи
    void rotateFace(char face, bool clockwise);

    // Проверка
    bool isSolved() const;

    // Ввод/игра
    void handleEvent(const sf::Event& event);
    void update();                        // обновляет анимацию
    void render(int width, int height);   // рисует сцену

    // ======= ТЕСТОВЫЕ УТИЛИТЫ (read-only, без побочек) =======
    // Сериализация состояния в строку (для сравнения в тестах/снапшотах)
    std::string serialize() const;
    // Хэш состояния (быстрое сравнение в тестах)
    std::uint64_t stateHash() const;

// Методы, доступные для тестирования
TESTABLE:
    // ======= утилиты модели =======
    static int  rotMapAxis(int v, char axis, bool cw);
    static void rotateOrientation(Cubelet& c, char axis, bool cw);

    // ======= анимация поворотов =======
    void startRotation(char face, bool cw);      // поставить в очередь/запустить
    void updateRotation(float dt);               // шаг анимации
    static bool isInLayer(int i,int j,int k, char face);
    static char faceAxis(char face);             // X/Y/Z
    static int  faceLayer(char face);            // 0 или 2

    // ======= рендер =======
    static void colorForWorldDir(const Cubelet& c, int worldDir, float& r, float& g, float& b);

// Приватные методы (не для тестирования)
private:
    // ======= состояние модели =======
    Cubelet cubie_[3][3][3];

    // ======= камера/анимация =======
    float angleX_ = 22.f, angleY_ = -30.f;
    float distZ_  = -10.f;
    bool  dragging_ = false;
    int   lastMouseX_ = 0, lastMouseY_ = 0;
    sf::Clock clock_;

    struct Rotation { char face; bool clockwise; float progress; bool active=false; };
    Rotation current_{};
    std::vector<Rotation> queue_;

    // ======= рендер (остаются полностью приватными) =======
    void setupProjection_(int width, int height);
    void drawCubelet_(const Cubelet& c, float cx, float cy, float cz, float size,
                      int i, int j, int k);
};
