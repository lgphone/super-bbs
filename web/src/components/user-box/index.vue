<template>
  <div class="box"
       v-if="!$user">
    <div class="cell">
      <div>
        <h4>v22x</h4>
      </div>
      <div style="color: #ccc;margin-top:5px;">这是另一个FakeV2EX</div>
    </div>
    <div class="inner">
      <div class="center"><Button to="/account/register">现在注册</Button></div>
      <div class="center"
           style="margin-top: 10px;">已注册用户请 <a class="a-link"
           href="/#/account/login">登录</a></div>
    </div>
  </div>
  <div class="box"
       v-else>
    <div class="cell">
      <div style="display: flex;">
        <div class="avatar"><a></a></div>
        <div style="flex-grow: 1;display: flex;margin-left: 10px;">
          <div style="display: flex;align-items:center"><a :href="`/#/member?username=${$user.username}`"
               class="a-link">{{$user.username}}</a></div>
        </div>
      </div>
      <div style="display: flex;justify-content:center;margin-top:10px;">
        <div style="text-align: center;">
          <a href="/#/my/nodes">
            <div>{{$user.fav_sub_tab_count}}</div>
            <div style="color: #ccc;">节点收藏</div>
          </a>
        </div>
        <div style="width: 1px;height: 35px; background: rgba(100, 100, 100, 0.4);margin: 0 10px;"></div>
        <div style="text-align: center;">
          <a href="/#/my/topics">
            <div>{{$user.fav_topic_count}}</div>
            <div style="color: #ccc;">主题收藏</div>
          </a>
        </div>
        <div style="width: 1px;height: 35px; background: rgba(100, 100, 100, 0.4);margin: 0 10px;"></div>
        <div style="text-align: center;">
          <a href="/#/my/following">
            <div>{{$user.fav_user_count}}</div>
            <div style="color: #ccc;">特别关注</div>
          </a>
        </div>
      </div>
    </div>
    <div class="cell">
      <div><a class="a-link"
           href="/#/new">
          <Icon type="ios-create-outline"
                size="18" />创作新主题</a></div>
    </div>
    <div class="cell">
      <div><a class="a-link">0 条未读提醒</a></div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'user-box'
}
</script>
