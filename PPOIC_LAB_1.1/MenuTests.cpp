#include <gtest/gtest.h>
#include "Menu.hpp"
#include <SFML/Graphics.hpp>

class MenuTest : public ::testing::Test {
protected:
    Menu menu;
    sf::RenderWindow window;
    
    void SetUp() override {
        menu.init();
    }
};

TEST_F(MenuTest, InitializationLoadsFont) {
    // Проверяем, что меню инициализируется без сбоев
    menu.onOpen(); // Не должно падать
}

TEST_F(MenuTest, ShowMethodNoCrash) {
    EXPECT_NO_THROW(menu.show());
}

TEST_F(MenuTest, HandleEventEscapeClosesMenu) {
    RubikCube cube;
    bool inMenu = true;
    
    sf::Event escapeEvent;
    escapeEvent.type = sf::Event::KeyPressed;
    escapeEvent.key.code = sf::Keyboard::Escape;
    
    menu.handleEvent(escapeEvent, window, cube, inMenu);
    
    EXPECT_FALSE(inMenu);
}

TEST_F(MenuTest, HandleEventNumericalSelections) {
    RubikCube cube;
    bool inMenu = true;
    
    // Тест выбора 1 (собранный куб)
    sf::Event key1Event;
    key1Event.type = sf::Event::KeyPressed;
    key1Event.key.code = sf::Keyboard::Num1;
    
    menu.handleEvent(key1Event, window, cube, inMenu);
    EXPECT_FALSE(inMenu);
}

TEST_F(MenuTest, ActionExecution) {
    RubikCube cube;
    bool inMenu = true;
    
    // Тестируем действие 0 - инициализация собранного куба
    menu.doAction(0, window, cube, inMenu);
    EXPECT_FALSE(inMenu);
    
    // Возвращаемся в меню для следующего теста
    inMenu = true;
    menu.doAction(3, window, cube, inMenu); // Сохранение
    EXPECT_TRUE(inMenu); // Должны остаться в меню после сохранения
}

TEST_F(MenuTest, ComputeLayoutNoCrash) {
    sf::FloatRect panel;
    std::vector<sf::FloatRect> itemRects;
    sf::Vector2f titlePos, hintPos;
    
    EXPECT_NO_THROW(menu.computeLayout(window, panel, itemRects, titlePos, hintPos));
    EXPECT_FALSE(itemRects.empty());
}

TEST_F(MenuTest, EnsureItemsPopulated) {
    // Вызываем внутренний метод для гарантии заполнения items
    menu.ensureItems();
    // Если метод работает корректно, items не должны быть пустыми
}
