import random


def get_ads():

    ADS = [
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=2830fc97eaa137f734e69d4396e4d010&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B0168IXO3M&asins=B0168IXO3M&linkId=254bbc9bfa0a4036f68a28fa012e606c&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=fc0b273e6e80698b17d08df8fe00db2f&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=fc0b273e6e80698b17d08df8fe00db2f&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B0752R48BJ&asins=B0752R48BJ&linkId=618bef88f12099155d3c7f67b77d21e0&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=2830fc97eaa137f734e69d4396e4d010&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B0168IXO3M&asins=B0168IXO3M&linkId=254bbc9bfa0a4036f68a28fa012e606c&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=fc0b273e6e80698b17d08df8fe00db2f&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=fc0b273e6e80698b17d08df8fe00db2f&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=2830fc97eaa137f734e69d4396e4d010&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B0168IXO3M&asins=B0168IXO3M&linkId=254bbc9bfa0a4036f68a28fa012e606c&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=fc0b273e6e80698b17d08df8fe00db2f&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=fc0b273e6e80698b17d08df8fe00db2f&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B0752R48BJ&asins=B0752R48BJ&linkId=618bef88f12099155d3c7f67b77d21e0&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=2830fc97eaa137f734e69d4396e4d010&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B0168IXO3M&asins=B0168IXO3M&linkId=254bbc9bfa0a4036f68a28fa012e606c&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=fc0b273e6e80698b17d08df8fe00db2f&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=fc0b273e6e80698b17d08df8fe00db2f&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=2830fc97eaa137f734e69d4396e4d010&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B0168IXO3M&asins=B0168IXO3M&linkId=254bbc9bfa0a4036f68a28fa012e606c&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=fc0b273e6e80698b17d08df8fe00db2f&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=fc0b273e6e80698b17d08df8fe00db2f&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B0752R48BJ&asins=B0752R48BJ&linkId=618bef88f12099155d3c7f67b77d21e0&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=2830fc97eaa137f734e69d4396e4d010&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B0168IXO3M&asins=B0168IXO3M&linkId=254bbc9bfa0a4036f68a28fa012e606c&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=fc0b273e6e80698b17d08df8fe00db2f&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=fc0b273e6e80698b17d08df8fe00db2f&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=2830fc97eaa137f734e69d4396e4d010&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B0168IXO3M&asins=B0168IXO3M&linkId=254bbc9bfa0a4036f68a28fa012e606c&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=fc0b273e6e80698b17d08df8fe00db2f&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=fc0b273e6e80698b17d08df8fe00db2f&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B0752R48BJ&asins=B0752R48BJ&linkId=618bef88f12099155d3c7f67b77d21e0&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=2830fc97eaa137f734e69d4396e4d010&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B0168IXO3M&asins=B0168IXO3M&linkId=254bbc9bfa0a4036f68a28fa012e606c&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=fc0b273e6e80698b17d08df8fe00db2f&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=fc0b273e6e80698b17d08df8fe00db2f&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=2830fc97eaa137f734e69d4396e4d010&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B0168IXO3M&asins=B0168IXO3M&linkId=254bbc9bfa0a4036f68a28fa012e606c&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=fc0b273e6e80698b17d08df8fe00db2f&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=fc0b273e6e80698b17d08df8fe00db2f&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B0752R48BJ&asins=B0752R48BJ&linkId=618bef88f12099155d3c7f67b77d21e0&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=2830fc97eaa137f734e69d4396e4d010&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B0168IXO3M&asins=B0168IXO3M&linkId=254bbc9bfa0a4036f68a28fa012e606c&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=fc0b273e6e80698b17d08df8fe00db2f&show_border=true&link_opens_in_new_window=true"></iframe>',
        '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=aibestgoods-20&language=en_US&marketplace=amazon&region=US&placement=B082VXK9CK&asins=B082VXK9CK&linkId=fc0b273e6e80698b17d08df8fe00db2f&show_border=true&link_opens_in_new_window=true"></iframe>',
    ]

    random.shuffle(ADS)

    return ADS
