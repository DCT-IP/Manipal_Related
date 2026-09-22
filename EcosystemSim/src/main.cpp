#include <iostream>
#include <optional>
#include <SFML/Graphics.hpp>

int main(){
    std::cout << "Before Opening" << std::endl;
    sf::Clock clock;
    sf::RectangleShape rect(sf::Vector2f(60.f,60.f));
    rect.setOrigin(30.f,30.f);
    rect.setPosition(100.f,300.f);
    float Velx = 150.f;
    sf::RenderWindow window(sf::VideoMode({800, 600}), "EcoSystemSim");
    while(window.isOpen()){
        sf::Time elapsed = clock.restart();
        float dt = elapsed.asSeconds();
        sf::Event event;
        while(window.pollEvent(event)){
            if (event.type == sf::Event::Closed)
                window.close();
        }
        rect.move(Velx * dt, 0.f);
        sf::Vector2f pos = rect.getPosition();
        if (pos.x > 770.f || pos.x < 30.f) {
            Velx = -Velx; 
        }
        window.clear(sf::Color::Black);
        window.draw(rect);
        window.display();
    }
    std::cout << "After Opening " << std::endl;
    return 0;
}