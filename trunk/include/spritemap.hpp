
#ifndef SPRITEMAP_HPP
#define SPRITEMAP_HPP

#include "util.hpp"

#include <map>
#include <set>
#include <string>

#include "singleton.hpp"


namespace opi2d
{
	class Sprite;
	
	typedef std::map<int, std::string> IdMap;
	
	class SpriteMapper : public Singleton<SpriteMapper>
	{
		public:
		void AddSprite(const std::string& type, Sprite* sprite);
		const std::string RemoveSprite(Sprite* sprite); 
		
		protected:
		
		friend class Singleton<SpriteMapper>;
		IdMap sprites;
	};
}

#endif

