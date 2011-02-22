
#ifndef SCENE_HPP
#define SCENE_HPP

#include "util.hpp"

#include <string>
#include <vector>
#include <map>
#include <set>
#include <utility>
#include <list>

#include "debug.hpp"
#include "color.hpp"
#include "vec.hpp"
#include "actions.hpp"

namespace opi2d
{
    class Layer;
    class SceneCallbacks;
    class SpriteGroup;
    class Light;
    class Camera;
    class Sprite;
        
    typedef std::list<Layer*> Layers;
    typedef std::map<std::string, Layer*> LayerMap;
    typedef std::map<std::string, SpriteGroup*> SpriteGroups;
    typedef std::pair<std::string, std::string> NamePair;
    typedef std::set<NamePair> Collisions;
    typedef std::set<Light*> Lights;
   
    class DLLEXPORT Scene
    {
        public:
        Scene();
        ~Scene();
        
        // Callbacks
        void SetCallbacks(SceneCallbacks* callback);
        SceneCallbacks* GetCallbacks();
        
        // Render all layers in scene
        void Render();
        
        // Scene logic handling
        void Tick();
        void RealTick();
        
        // Scene initialization
        void AddLayer(const std::string& name);
        void DeleteLayer(const std::string& name);
        void DeleteLayer(Layer* layer);
        Layers GetLayers();
        void SetLayers( Layers layers);
        
        SpriteGroup* GetGroup(const std::string& name);
        SpriteGroup* CreateGroup(const std::string& name);        
        
        void EnableCollisions(const std::string& group1, const std::string& group2);
        void DisableAllCollisions();
        
        void AddLight(Light* light);
        void RemoveLight(Light* light);
        void SetAmbientLight(const Color& color);
        
        inline const Lights& GetLights() { return lights; }
        Color CalculateLight(const Vec2& pos);
        
        inline Layer* GetLayer(const std::string& name)
        {
            return this->namemap[name];
        }
        
        inline Camera* GetCamera() { return this->camera; }
        
        // Action Handling
        void AddAction(Action* action);
        void RemoveAction(Action* action);
        
        protected:
            
        void update_lights();
        
        Camera* camera;
        
        Layers layers;
        LayerMap namemap;
        SpriteGroups groups;
        SceneCallbacks* callbacks;
        Collisions collisions;
        Lights lights;
        Color ambient_light;
        
        ActionManager manager;
    };
    
    class DLLEXPORT SceneCallbacks
    {
        public:
        SceneCallbacks() {FUNC}
        virtual ~SceneCallbacks() {FUNC}
                    
        virtual void OnCollision(const std::string& group1, const std::string& group2, Sprite* sprite1, Sprite* sprite2) {}
    };
}


#endif

