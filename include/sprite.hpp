
#ifndef OPISPRITE
#define OPISPRITE

#include "util.hpp"

#include <set>
#include <string>
#include <vector>

#include "node.hpp"
#include "vec.hpp"
#include "color.hpp"
#include "area.hpp"
#include "collision.hpp"
#include "mutators.hpp"

namespace opi2d
{
    class Image;
    class SpriteGroup;
        
    typedef std::set<SpriteGroup*> GroupSet;
    
    class DLLEXPORT Sprite : public Node
    {
        public:
		virtual void VM_SetProp(ExecFrame* f, int idx);
		virtual void VM_GetProp(ExecFrame* f, int idx);
		virtual void VM_MetCall(ExecFrame* f, int idx);
        
        
        Sprite(const Image* image=NULL);
        virtual ~Sprite();
        
        virtual void Delete();
        virtual void ReUse();
               
        void SetImage(const Image* image);

        void Enter();
        void EnterFree();
        
        void JoinGroup(SpriteGroup* group);
        void LeaveGroup(SpriteGroup* group);
        
        //void AddCollisionNode(float radius, float x=0, float y=0);
        
        inline int GetLightingDetail() { return lighting_detail; }
        inline void SetLightingDetail(int detail) { lighting_detail = detail; }
        
        inline void EnableLighting(bool flag) { enable_lighting = flag; }
        
        void TransformCollisionNodes();
        
        Rect GetRect() const;
        Rect GetWorldRect() const;
        FreeRect GetTransformedRect() const;
        
        Sprite* PickSelf(const Vec2& p);

        protected:
        
	    void CalculateQuad(floatval x, floatval y, const Image* image, quad_vertices& va, quad_vertices& ta, quad_colors& ca) const;
		void RenderQuad(floatval x, floatval y, const Image* image, quad_vertices& va, quad_vertices& ta, quad_colors& ca) const;	    
		void RenderFree(floatval x, floatval y, const Image* image, quad_vertices& va, quad_vertices& ta, quad_colors& ca) const;	    

        int lighting_detail;
        bool enable_lighting;

        friend class SpriteGroup;
        friend class Scene;
        const Image* image;

        GroupSet groups;
        CollisionNodes collnodes;
        int coll_transform_tick;
    };
    
    typedef std::set<Sprite*> SpriteSet;
    
    class DLLEXPORT SpriteGroup
    {
        public:
        SpriteGroup(const std::string& name);
        ~SpriteGroup();
        
        void AddSprite(Sprite* sprite);
        void RemoveSprite(Sprite* sprite);
        void AddMutator(Mutator* mutator);
        
        void Tick();
        
        void Lock() { this->iterating = true; }
        void Unlock() { this->iterating = false; this->ClearBuffers(); }
        
        inline int GetSize() const { return this->sprites.size(); }
        
        std::vector<Sprite*> ListSprites() const;
        
        Sprite* Pick(const Vec2& p) const; 
        
        void ClearBuffers();
        
        SpriteSet::iterator Begin();
        SpriteSet::iterator End();
        
        protected:
        std::string name;
        SpriteSet sprites;
        
        bool iterating;
        SpriteSet to_be_deleted;
        SpriteSet to_be_added;
        mutatorlist mutators;
    };

}

#endif

