#include <iostream>
#include <optional>
#include <SFML/Graphics.hpp>

int main(){
    std::cout << "Before Opening" << std::endl;
    sf::RenderWindow window(sf::VideoMode({800, 600}), "EcoSystemSim");
    while(window.isOpen()){
        sf::Event event;
        while(window.pollEvent(event)){
            if (event.type == sf::Event::Closed)
                window.close();
        }
        window.clear(sf::Color::Black);
        window.display();
    }
    std::cout << "After Opening " << std::endl;
    return 0;
}