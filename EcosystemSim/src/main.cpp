#include <iostream>
#include <optional>
#include <SFML/Graphics.hpp>
#include <SFML/Graphics/Transformable.hpp>


int main(){
    std::cout << "Before Opening" << std::endl;
    float VelX = 150.f;
    float rot = 45.f;
    sf::Clock clock;
    sf::RectangleShape rect1(sf::Vector2f(50.f,50.f));
    rect1.setPosition(0.f,0.f);
    rect1.setOrigin(0.f,0.f);
    rect1.setFillColor(sf::Color::Red);
    sf::RectangleShape rect2(sf::Vector2f(50.f,50.f));
    rect2.setPosition(100.f,0.f);
    rect1.setOrigin(100.f,0.f);
    rect2.setFillColor(sf::Color::Blue);
    sf::RectangleShape rect3(sf::Vector2f(50.f,50.f));
    rect1.setOrigin(100.f,100.f);
    rect3.setPosition(100.f,100.f);
    rect3.setFillColor(sf::Color::Green);
    sf::RenderWindow window(sf::VideoMode({800, 600}), "EcoSystemSim");
    while (window.isOpen())
    {
        sf::Time elapsed = clock.restart();
        float dt = elapsed.asSeconds();
        sf::Event event;
        while(window.pollEvent(event)){
            if (event.type == sf::Event::Closed)
                window.close();
        }
        rect1.move(VelX*dt, 0.f);
        rect2.move(VelX*dt, 0.f);
        rect3.move(VelX*dt, 0.f);
        rect1.rotate(rot*dt);
        rect2.rotate(rot*dt);
        rect3.rotate(rot*dt);
        sf::Vector2f pos1 = rect1.getPosition();
        sf::Vector2f pos2 = rect2.getPosition();
        sf::Vector2f pos3 = rect3.getPosition();
        if (pos1.x > 770.f || pos1.x < 30.f) {
            VelX = -VelX; 
        }
        if (pos3.x > 770.f || pos3.x < 30.f) {
            VelX = -VelX; 
        }
        if (pos2.x > 770.f || pos2.x < 30.f) {
            VelX = -VelX; 
        }
        window.clear(sf::Color::Black);
        window.draw(rect1);
        window.draw(rect2);
        window.draw(rect3);
        window.display();
    }
    
    std::cout << "After Opening " << std::endl;
    return 0;
}