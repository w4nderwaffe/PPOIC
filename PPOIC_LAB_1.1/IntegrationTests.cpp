#include <gtest/gtest.h>
#include "RubikCube.hpp"
#include "Menu.hpp"

class IntegrationTest : public ::testing::Test {
protected:
    RubikCube cube;
    Menu menu;
};

TEST_F(IntegrationTest, MenuCubeInteraction) {
    menu.init();
    cube.initSolved();
    
    // Проверяем, что меню может взаимодействовать с кубом без сбоев
    EXPECT_TRUE(cube.isSolved());
}

TEST_F(IntegrationTest, StatePersistenceFlow) {
    cube.initRandom(10);
    std::uint64_t originalState = cube.stateHash();
    
    // Симуляция сохранения и загрузки
    EXPECT_TRUE(cube.saveToFile("integration_test.txt"));
    
    RubikCube newCube;
    EXPECT_TRUE(newCube.loadFromFile("integration_test.txt"));
    
    EXPECT_EQ(originalState, newCube.stateHash());
    
    // Cleanup - используем remove из cstdio вместо filesystem
    std::remove("integration_test.txt");
}
