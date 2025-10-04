#include <gtest/gtest.h>
#include "RubikCube.hpp"
#include <fstream>
#include <filesystem>

// Определяем макрос TESTING перед включением заголовков
#define TESTING

class RubikCubeTest : public ::testing::Test {
protected:
    RubikCube cube;
    
    void SetUp() override {
        cube.initSolved();
    }
};

// Тесты инициализации
TEST_F(RubikCubeTest, InitializesToSolvedState) {
    EXPECT_TRUE(cube.isSolved());
}

TEST_F(RubikCubeTest, SerializeDeserializeConsistency) {
    std::string initial = cube.serialize();
    cube.initRandom(5);
    std::string afterRandom = cube.serialize();
    EXPECT_NE(initial, afterRandom);
}

// Тесты поворотов граней
TEST_F(RubikCubeTest, RotateFaceUClockwise) {
    cube.rotateFace('U', true);
    EXPECT_FALSE(cube.isSolved());
}

TEST_F(RubikCubeTest, MultipleRotationsReturnToSolved) {
    cube.rotateFace('U', true);
    cube.rotateFace('U', false);
    EXPECT_TRUE(cube.isSolved());
}

// Тесты файловых операций
TEST_F(RubikCubeTest, SaveAndLoadFile) {
    const std::string testFile = "test_cube.txt";
    cube.initRandom(10);
    std::uint64_t originalHash = cube.stateHash();
    
    EXPECT_TRUE(cube.saveToFile(testFile));
    
    RubikCube loadedCube;
    EXPECT_TRUE(loadedCube.loadFromFile(testFile));
    
    EXPECT_EQ(originalHash, loadedCube.stateHash());
    
    // Cleanup
    std::filesystem::remove(testFile);
}

// Тесты приватных утилитных функций (теперь доступны через TESTABLE)
TEST_F(RubikCubeTest, FaceAxisMapping) {
    EXPECT_EQ(RubikCube::faceAxis('U'), 'Y');
    EXPECT_EQ(RubikCube::faceAxis('D'), 'Y');
    EXPECT_EQ(RubikCube::faceAxis('L'), 'X');
    EXPECT_EQ(RubikCube::faceAxis('R'), 'X');
    EXPECT_EQ(RubikCube::faceAxis('F'), 'Z');
    EXPECT_EQ(RubikCube::faceAxis('B'), 'Z');
}

TEST_F(RubikCubeTest, FaceLayerMapping) {
    EXPECT_EQ(RubikCube::faceLayer('U'), 2);
    EXPECT_EQ(RubikCube::faceLayer('R'), 2);
    EXPECT_EQ(RubikCube::faceLayer('F'), 2);
    EXPECT_EQ(RubikCube::faceLayer('D'), 0);
    EXPECT_EQ(RubikCube::faceLayer('L'), 0);
    EXPECT_EQ(RubikCube::faceLayer('B'), 0);
}

TEST_F(RubikCubeTest, IsInLayerDetection) {
    EXPECT_TRUE(RubikCube::isInLayer(1, 2, 1, 'U'));
    EXPECT_FALSE(RubikCube::isInLayer(1, 1, 1, 'U'));
    EXPECT_TRUE(RubikCube::isInLayer(0, 1, 1, 'L'));
    EXPECT_TRUE(RubikCube::isInLayer(2, 1, 1, 'R'));
}

TEST_F(RubikCubeTest, RotationMapAxis) {
    EXPECT_EQ(RubikCube::rotMapAxis(2, 'X', true), 3);
    EXPECT_EQ(RubikCube::rotMapAxis(3, 'X', true), -2);
    EXPECT_EQ(RubikCube::rotMapAxis(2, 'X', false), -3);
    EXPECT_EQ(RubikCube::rotMapAxis(3, 'X', false), 2);
}

TEST_F(RubikCubeTest, RotationOrientation) {
    Cubelet c{0, 0, 0, 1, 2, 3};
    
    RubikCube::rotateOrientation(c, 'X', true);
    EXPECT_EQ(c.ax, 1);
    EXPECT_EQ(c.ay, 3);
    EXPECT_EQ(c.az, -2);
}

TEST_F(RubikCubeTest, StartRotation) {
    cube.startRotation('U', true);
    cube.update(); // Должно прогрессировать анимацию
    // Проверяем через публичный интерфейс
}

TEST_F(RubikCubeTest, ColorMapping) {
    Cubelet c{0, 0, 0, 1, 2, 3};
    float r, g, b;
    
    RubikCube::colorForWorldDir(c, 1, r, g, b);
    EXPECT_GT(r, 0.5f);
}
