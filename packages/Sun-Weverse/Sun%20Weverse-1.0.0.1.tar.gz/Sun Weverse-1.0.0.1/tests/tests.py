import asyncio
import json

import pytest
from sunverse.enums import ObjectTypes, PostTypes
from sunverse.objects.artist import Artist
from sunverse.objects.community import Community
from sunverse.objects.media import ImageMedia, WeverseMedia, YoutubeMedia
from sunverse.objects.notification import Notification
from sunverse.sunverse import SunverseClient


class TestSunverse:
    sunverse_client = SunverseClient("anson_2012@yahoo.com", "BearBear123!")

    @pytest.mark.asyncio
    async def test_fetch_joined_communities(self):
        """This test is to ensure that this API wrapper is kept up-to-date with
        the data structure provided by Weverse's API.

        Notes
        -----
        It is best recommended to test this with an account that has
        joined all the communities to ensure no special cases arise.
        This test makes 1 request to the Weverse API per community the
        account used is part of.
        """

        await self.sunverse_client._fetch_access_token_by_credentials()
        required_keys = [
            "communityId",
            "communityName",
            "communityAlias",
            "urlPath",
            "logoImage",
            "homeHeaderImage",
            "homeGradationColor",
            "hasMembershipProduct",
            "availableActions",
            "agencyProfile",
            "birthdayArtists",
        ]
        optional_keys = ["artistCode", "fandomName", "fanEventUrl", "memberCount"]
        agency_profile_keys = ["profileImageUrl", "profileName", "profileCoverImageUrl"]
        successful = True

        joined_communities = await self.sunverse_client.fetch_joined_communities()

        for joined_community in joined_communities:
            for required_key in required_keys:
                if required_key not in joined_community.data:
                    raise KeyError(
                        f"{required_key} does not exist in {joined_community.name}."
                    )

            for key in joined_community.data:
                if key not in optional_keys and key not in required_keys:
                    raise KeyError(
                        f"{key} is neither an optional key, nor a required key - "
                        "which means that it's a new key added on Weverse's side and "
                        "an update to the Community class is required."
                    )

            for agency_profile_key in agency_profile_keys:
                if agency_profile_key not in joined_community.data["agencyProfile"]:
                    raise KeyError(
                        f"{agency_profile_key} does not exist in the agencyProfile "
                        f"of {joined_community.name}."
                    )

            for c_agency_profile_key in joined_community.data["agencyProfile"]:
                if c_agency_profile_key not in agency_profile_keys:
                    raise KeyError(
                        f"{c_agency_profile_key} is not a agency profile key - "
                        "which means that it's a new key added on Weverse's side and "
                        "an update to the Community class is required."
                    )

        assert successful

    @pytest.mark.asyncio
    async def test_fetch_latest_notifications(self):
        """This test is to ensure that this API wrapper is kept up-to-date with
        the data structure provided by Weverse's API.
        """

        required_keys = [
            "activityId",
            "read",
            "messageId",
            "title",
            "message",
            "logoImageUrl",
            "webUrl",
            "time",
            "count",
            "community",
            "type",
        ]
        useless_keys = ["scheme"]
        optional_keys = ["imageUrl", "authors", "compactedMessageMap", "createDate"]
        successful = True

        latest_notifications = await self.sunverse_client.fetch_latest_notifications()

        for latest_notification in latest_notifications:
            for required_key in required_keys:
                if required_key not in latest_notification.data:
                    raise KeyError(
                        f"{required_key} does not exist in {latest_notification.id}."
                    )

            for key in latest_notification.data:
                if (
                    key not in optional_keys
                    and key not in required_keys
                    and key not in useless_keys
                ):
                    raise KeyError(
                        f"{key} is neither an optional key, nor a required key - "
                        "which means that it's a new key added on Weverse's side and "
                        "an update to the Notification class is required."
                    )

        assert successful

    '''@pytest.mark.asyncio
    async def test_posts(self):
        """This test is to ensure that this API wrapper is kept up-to-date with
        the data structure provided by Weverse's API."""
        loop = 0
        start = True
        successful = True
        notifications = await self.sunverse_client.fetch_latest_notifications()
        required_keys = [
            "extension",
            "shareUrl",
            "bookmarked",
            "locked",
            "hasProduct",
            "attachment",
            "body",
            "tags",
            "availableActions",
            "postType",
            "sectionType",
            "publishedAt",
            "hideFromArtist",
            "membershipOnly",
            "commentCount",
            "postId",
            "emotionCount",
            "plainBody",
            "author",
            "community",
        ]
        attachment_keys = ["photo", "video"]
        optional_keys = ["artistReactions", "viewerEmotionId"]

        while loop <= 100:
            if not start:
                await asyncio.sleep(0.25)
                data = await self.sunverse_client._fetcher(self.sunverse_client._urls.latest_notifications_url())
                data = await self.sunverse_client._fetcher(self.sunverse_client._urls.notification_url(int(data["paging"]["nextParams"]["after"])))
                notifications = [await self.sunverse_client._object_creator(ObjectTypes.NOTIFICATION, d, self.sunverse_client._urls.notification_url(int(data["paging"]["nextParams"]["after"]))) for d in data["data"] if d.get("community")]

            for notification in notifications:
                await asyncio.sleep(0.25)
                if notification.post_type != PostTypes.POST:
                    continue

                post = await self.sunverse_client.fetch_post(notification.post_id)

                for required_key in required_keys:
                    if required_key not in post.data:
                        raise KeyError(
                            f"Required Key: {required_key} does not exist "
                            f"in the fetched data for {post.url}"
                        )

                for key in post.data:
                    if key not in required_keys and key not in optional_keys:
                        raise KeyError(
                            f"Undefined Key: {key} does not exist in the required "
                            f"keys list and optional keys list for {post.url} - "
                            "which means that it's a new key added on Weverse's side and "
                            "an update to the Post class is required."
                        )

                for attachment_key in post.data["attachment"]:
                    if attachment_key not in attachment_keys:
                        raise KeyError(
                            f"Undefined Attachment Key: {attachment_key} does not "
                            f"exist in the attachment keys list for {post.url}"
                        )

            start = False
            loop += 1

        assert successful

    @pytest.mark.asyncio
    async def test_medias(self):
        """This test is to ensure that this API wrapper is kept up-to-date with
        the data structure provided by Weverse's API."""
        loop = 0
        start = True
        successful = True
        notifications = await self.sunverse_client.fetch_latest_notifications()
        required_keys = [
            "extension",
            "shareUrl",
            "bookmarked",
            "locked",
            "hasProduct",
            "attachment",
            "title",
            "body",
            "tags",
            "availableActions",
            "postType",
            "sectionType",
            "publishedAt",
            "hideFromArtist",
            "membershipOnly",
            "commentCount",
            "postId",
            "emotionCount",
            "plainBody",
            "author",
            "community",
        ]
        attachment_keys = ["photo", "video"]
        optional_keys = ["artistReactions", "viewerEmotionId"]

        while loop <= 100:
            if not start:
                await asyncio.sleep(0.25)
                data = await self.sunverse_client._fetcher(self.sunverse_client._urls.latest_notifications_url())
                data = await self.sunverse_client._fetcher(self.sunverse_client._urls.notification_url(int(data["paging"]["nextParams"]["after"])))
                notifications = [await self.sunverse_client._object_creator(ObjectTypes.NOTIFICATION, d, self.sunverse_client._urls.notification_url(int(data["paging"]["nextParams"]["after"]))) for d in data["data"] if d.get("community")]

            for notification in notifications:
                await asyncio.sleep(0.25)
                if notification.post_type != PostTypes.MEDIA:
                    continue

                media = await self.sunverse_client.fetch_media(notification.post_id)

                if media:
                    for required_key in required_keys:
                        if required_key not in media.data:
                            raise KeyError(
                                f"Required Key: {required_key} does not exist "
                                f"in the fetched data for {media.url}"
                            )

                    for key in media.data:
                        if key not in required_keys and key not in optional_keys:
                            raise KeyError(
                                f"Undefined Key: {key} does not exist in the required "
                                f"keys list and optional keys list for {media.url} - "
                                "which means that it's a new key added on Weverse's side and "
                                "an update to the Media class is required."
                            )

                    for attachment_key in media.data["attachment"]:
                        if attachment_key not in attachment_keys:
                            raise KeyError(
                                f"Undefined Attachment Key: {attachment_key} does not "
                                f"exist in the attachment keys list for {media.url}"
                            )

                    if isinstance(media, ImageMedia):
                        extra_required_keys = ["mediaInfo", "image"]

                        for extra_required_key in extra_required_keys:
                            if extra_required_key not in media.data["extension"]:
                                raise KeyError(
                                    f"Required Extra Key: {extra_required_key} does "
                                    f"not exist in the fetched data for {media.url}."
                                )

                        for extra_key in media.data["extension"]:
                            if extra_key not in extra_required_keys:
                                raise KeyError(
                                    f"Undefined Extra Key: {extra_key} does not exist "
                                    f"in the extra required keys list for {media.url} - "
                                    "which means that it's a new key added on Weverse's side "
                                    "and an update to the Media class is required."
                                )

                        required_media_keys = ["mediaType", "title", "body", "thumbnail", "categories"]

                        for required_media_key in required_media_keys:
                            if required_media_key not in media.data["extension"]["mediaInfo"]:
                                raise KeyError(
                                    f"Required Media Key: {required_media_key} does "
                                    f"not exist in the fetched data for {media.url}."
                                )

                        for media_key in media.data["extension"]["mediaInfo"]:
                            if media_key not in required_media_keys:
                                raise KeyError(
                                    f"Undefined Media Key: {media_key} does not exist "
                                    f"in the required media keys list for {media.url} - "
                                    "which means that it's a new key added on Weverse's side "
                                    "and an update to the Media class is required."
                                )

                        required_image_keys = ["photoCount", "photos", "viewType"]

                        for required_image_key in required_image_keys:
                            if required_image_key not in media.data["extension"]["image"]:
                                raise KeyError(
                                    f"Required Image Key: {required_image_key} does "
                                    f"not exist in the fetched data for {media.url}."
                                )

                        for image_key in media.data["extension"]["image"]:
                            if image_key not in required_image_keys:
                                raise KeyError(
                                    f"Undefined Image Key: {image_key} does not exist "
                                    f"in the required image keys list for {media.url} - "
                                    "which means that it's a new key added on Weverse's side "
                                    "and an update to the Media class is required."
                                )

                    if isinstance(media, WeverseMedia):
                        extra_required_keys = ["mediaInfo", "video"]

                        for extra_required_key in extra_required_keys:
                            if extra_required_key not in media.data["extension"]:
                                raise KeyError(
                                    f"Required Extra Key: {extra_required_key} does "
                                    f"not exist in the fetched data for {media.url}."
                                )

                        for extra_key in media.data["extension"]:
                            if extra_key not in extra_required_keys:
                                raise KeyError(
                                    f"Undefined Extra Key: {extra_key} does not exist "
                                    f"in the extra required keys list for {media.url} - "
                                    "which means that it's a new key added on Weverse's side "
                                    "and an update to the Media class is required."
                                )

                        required_media_keys = ["mediaType", "title", "body", "thumbnail", "categories"]

                        for required_media_key in required_media_keys:
                            if required_media_key not in media.data["extension"]["mediaInfo"]:
                                raise KeyError(
                                    f"Required Media Key: {required_media_key} does "
                                    f"not exist in the fetched data for {media.url}."
                                )

                        for media_key in media.data["extension"]["mediaInfo"]:
                            if media_key not in required_media_keys:
                                raise KeyError(
                                    f"Undefined Media Key: {media_key} does not exist "
                                    f"in the required media keys list for {media.url} - "
                                    "which means that it's a new key added on Weverse's side "
                                    "and an update to the Media class is required."
                                )

                        required_video_keys = [
                            "videoId",
                            "type",
                            "onAirStartAt",
                            "paid",
                            "membershipOnly",
                            "screenOrientation",
                            "thumb",
                            "previewType",
                            "playCount",
                            "likeCount",
                            "serviceName",
                            "serviceId",
                            "liveToVod",
                            "infraVideoId",
                            "playTime",
                            "encodingStatus"
                        ]

                        for required_video_key in required_video_keys:
                            if required_video_key not in media.data["extension"]["video"]:
                                raise KeyError(
                                    f"Required Video Key: {required_video_key} does "
                                    f"not exist in the fetched data for {media.url}."
                                )

                        for video_key in media.data["extension"]["video"]:
                            if video_key not in required_video_keys:
                                raise KeyError(
                                    f"Undefined Video Key: {video_key} does not exist "
                                    f"in the required video keys list for {media.url} - "
                                    "which means that it's a new key added on Weverse's side "
                                    "and an update to the Media class is required."
                                )

                    if isinstance(media, YoutubeMedia):
                        extra_required_keys = ["mediaInfo", "youtube"]

                        for extra_required_key in extra_required_keys:
                            if extra_required_key not in media.data["extension"]:
                                raise KeyError(
                                    f"Required Extra Key: {extra_required_key} does "
                                    f"not exist in the fetched data for {media.url}."
                                )

                        for extra_key in media.data["extension"]:
                            if extra_key not in extra_required_keys:
                                raise KeyError(
                                    f"Undefined Extra Key: {extra_key} does not exist "
                                    f"in the extra required keys list for {media.url} - "
                                    "which means that it's a new key added on Weverse's side "
                                    "and an update to the Media class is required."
                                )

                        required_media_keys = ["mediaType", "title", "body", "thumbnail", "categories"]

                        for required_media_key in required_media_keys:
                            if required_media_key not in media.data["extension"]["mediaInfo"]:
                                raise KeyError(
                                    f"Required Media Key: {required_media_key} does "
                                    f"not exist in the fetched data for {media.url}."
                                )

                        for media_key in media.data["extension"]["mediaInfo"]:
                            if media_key not in required_media_keys:
                                raise KeyError(
                                    f"Undefined Media Key: {media_key} does not exist "
                                    f"in the required media keys list for {media.url} - "
                                    "which means that it's a new key added on Weverse's side "
                                    "and an update to the Media class is required."
                                )

                        required_youtube_keys = [
                            "screenOrientation",
                            "playTime",
                            "videoPath",
                        ]

                        for required_youtube_key in required_youtube_keys:
                            if required_youtube_key not in media.data["extension"]["youtube"]:
                                raise KeyError(
                                    f"Required Youtube Key: {required_youtube_key} does "
                                    f"not exist in the fetched data for {media.url}."
                                )

                        for youtube_key in media.data["extension"]["youtube"]:
                            if youtube_key not in required_youtube_keys:
                                raise KeyError(
                                    f"Undefined Youtube Key: {youtube_key} does not exist "
                                    f"in the required youtube keys list for {media.url} - "
                                    "which means that it's a new key added on Weverse's side "
                                    "and an update to the Media class is required."
                                )

            start = False
            loop += 1

        assert successful

    @pytest.mark.asyncio
    async def test_lives(self):
        """This test is to ensure that this API wrapper is kept up-to-date with
        the data structure provided by Weverse's API."""
        loop = 0
        start = True
        successful = True
        notifications = await self.sunverse_client.fetch_latest_notifications()
        required_keys = [
            "extension",
            "shareUrl",
            "bookmarked",
            "locked",
            "hasProduct",
            "attachment",
            "title",
            "body",
            "tags",
            "availableActions",
            "postType",
            "sectionType",
            "publishedAt",
            "hideFromArtist",
            "membershipOnly",
            "commentCount",
            "postId",
            "emotionCount",
            "plainBody",
            "author",
            "community",
        ]
        attachment_keys = ["photo", "video"]
        optional_keys = ["artistReactions", "viewerEmotionId"]

        while loop <= 100:
            if not start:
                await asyncio.sleep(0.25)
                data = await self.sunverse_client._fetcher(self.sunverse_client._urls.latest_notifications_url())
                data = await self.sunverse_client._fetcher(self.sunverse_client._urls.notification_url(int(data["paging"]["nextParams"]["after"])))
                notifications = [await self.sunverse_client._object_creator(ObjectTypes.NOTIFICATION, d, self.sunverse_client._urls.notification_url(int(data["paging"]["nextParams"]["after"]))) for d in data["data"] if d.get("community")]

            for notification in notifications:
                await asyncio.sleep(0.25)
                if notification.post_type != PostTypes.LIVE:
                    continue

                live = await self.sunverse_client.fetch_live(notification.post_id)

                if live:
                    for required_key in required_keys:
                        if required_key not in live.data:
                            raise KeyError(
                                f"Required Key: {required_key} does not exist "
                                f"in the fetched data for {live.url}"
                            )

                    for key in live.data:
                        if key not in required_keys and key not in optional_keys:
                            raise KeyError(
                                f"Undefined Key: {key} does not exist in the required "
                                f"keys list and optional keys list for {live.url} - "
                                "which means that it's a new key added on Weverse's side and "
                                "an update to the Live class is required."
                            )

                    for attachment_key in live.data["attachment"]:
                        if attachment_key not in attachment_keys:
                            raise KeyError(
                                f"Undefined Attachment Key: {attachment_key} does not "
                                f"exist in the attachment keys list for {live.url}"
                            )

                    extra_required_keys = ["mediaInfo", "video"]

                    for extra_required_key in extra_required_keys:
                        if extra_required_key not in live.data["extension"]:
                            raise KeyError(
                                f"Required Extra Key: {extra_required_key} does "
                                f"not exist in the fetched data for {live.url}."
                            )

                    for extra_key in live.data["extension"]:
                        if extra_key not in extra_required_keys:
                            raise KeyError(
                                f"Undefined Extra Key: {extra_key} does not exist "
                                f"in the extra required keys list for {live.url} - "
                                "which means that it's a new key added on Weverse's side "
                                "and an update to the Live class is required."
                            )

                    required_media_keys = ["mediaType", "title", "body", "thumbnail", "chat"]
                    optional_media_keys = ["categories"]

                    for required_media_key in required_media_keys:
                        if required_media_key not in live.data["extension"]["mediaInfo"]:
                            raise KeyError(
                                f"Required Media Key: {required_media_key} does "
                                f"not exist in the fetched data for {live.url}."
                            )

                    for media_key in live.data["extension"]["mediaInfo"]:
                        if media_key not in required_media_keys and media_key not in optional_media_keys:
                            raise KeyError(
                                f"Undefined Media Key: {media_key} does not exist "
                                f"in the required media keys list for {live.url} - "
                                "which means that it's a new key added on Weverse's side "
                                "and an update to the Live class is required."
                            )

                    required_video_keys = [
                        "videoId",
                        "type",
                        "onAirStartAt",
                        "paid",
                        "membershipOnly",
                        "screenOrientation",
                        "thumb",
                        "previewType",
                        "playCount",
                        "likeCount",
                        "serviceName",
                        "serviceId",
                        "liveToVod",
                        "infraVideoId",
                        "playTime",
                        "encodingStatus"
                    ]

                    for required_video_key in required_video_keys:
                        if required_video_key not in live.data["extension"]["video"]:
                            raise KeyError(
                                f"Required Video Key: {required_video_key} does "
                                f"not exist in the fetched data for {live.url}."
                            )

                    for video_key in live.data["extension"]["video"]:
                        if video_key not in required_video_keys:
                            raise KeyError(
                                f"Undefined Video Key: {video_key} does not exist "
                                f"in the required video keys list for {live.url} - "
                                "which means that it's a new key added on Weverse's side "
                                "and an update to the Live class is required."
                            )

            start = False
            loop += 1

        assert successful'''

    @pytest.mark.asyncio
    async def test_notices(self):
        """This test is to ensure that this API wrapper is kept up-to-date with
        the data structure provided by Weverse's API."""
        loop = 0
        start = True
        successful = True
        notifications = await self.sunverse_client.fetch_latest_notifications()
        required_keys = [
            "pinned",
            "noticeId",
            "exposed",
            "title",
            "body",
            "noticeType",
            "published",
            "parentId",
            "hideFromArtist",
            "membershipOnly",
            "publishAt",
            "exposedStatus",
            "plainBody",
            "attachment",
            "shareUrl",
            "appUrl",
        ]
        attachment_keys = ["photo", "video"]

        while loop <= 100:
            if not start:
                await asyncio.sleep(0.25)
                data = await self.sunverse_client._fetcher(self.sunverse_client._urls.latest_notifications_url())
                data = await self.sunverse_client._fetcher(self.sunverse_client._urls.notification_url(int(data["paging"]["nextParams"]["after"])))
                notifications = [await self.sunverse_client._object_creator(ObjectTypes.NOTIFICATION, d, self.sunverse_client._urls.notification_url(int(data["paging"]["nextParams"]["after"]))) for d in data["data"] if d.get("community")]

            for notification in notifications:
                await asyncio.sleep(0.25)
                if notification.post_type != PostTypes.NOTICE:
                    continue

                notice = await self.sunverse_client.fetch_notice(notification.post_id)

                for required_key in required_keys:
                    if required_key not in notice.data:
                        raise KeyError(
                            f"Required Key: {required_key} does not exist "
                            f"in the fetched data for {notice.url}"
                        )

                for key in notice.data:
                    if key not in required_keys:
                        raise KeyError(
                            f"Undefined Key: {key} does not exist in the required "
                            f"keys list for {notice.url} - which means that it's a "
                            "new key added on Weverse's side and "
                            "an update to the Notice class is required."
                        )

                for attachment_key in notice.data["attachment"]:
                    if attachment_key not in attachment_keys:
                        raise KeyError(
                            f"Undefined Attachment Key: {attachment_key} does not "
                            f"exist in the attachment keys list for {notice.url}"
                        )

        start = False
        loop += 1

        assert successful

"""async def test(self):
        while True:
            if not start:
                if post.data["membershipOnly"] == True:
                    print(f"Key: membershipOnly is True in {post.url}")

                if post.data["hideFromArtist"] == True:
                    print(f"Key: hideFromArtist is True in {post.url}")

                if post.data["hasProduct"] == True:
                    print(f"Key: hasProduct is True in {post.url}")

                if post.data["locked"] == True:
                    print(f"Key: locked is True in {post.url}")

                if post.data["sectionType"] != "ARTIST":
                    print(f"Key: sectionType is not ARTIST in {post.url}")

                if post.data["postType"] != "NORMAL":
                    print(f"Key: postType is not NORMAL in {post.url}")

                if post.data["tags"]:
                    print(f"Key: tags is not empty in {post.url}")

                if post.data["extension"]:
                    print(f"Key: extension is not empty in {post.url}")

            start = False
            loop += 1

    async def test_two(self):
        start = True
        loop = 0
        data = (await self._fetcher(self._urls.latest_fan_posts_url(47)))["feedTabPosts"]
        required_keys = [
            "extension",
            "shareUrl",
            "bookmarked",
            "locked",
            "hasProduct",
            "attachment",
            "body",
            "tags",
            "availableActions",
            "postType",
            "sectionType",
            "publishedAt",
            "hideFromArtist",
            "membershipOnly",
            "commentCount",
            "postId",
            "emotionCount",
            "plainBody",
            "author",
            "community",
        ]
        attachment_keys = ["photo", "video"]
        optional_keys = ["artistReactions", "viewerEmotionId"]

        while True:
            if not start:
                data = await self._fetcher(self._urls.test_url(data["paging"]["nextParams"]["after"]))

            for d in data["data"]:
                await asyncio.sleep(0.5)
                post = await self.fetch_post(d["postId"])

                for required_key in required_keys:
                    if required_key not in post.data:
                        print(f"Required Key: {required_key} does not exist in the fetched data for {post.url}")

                for key in post.data:
                    if key not in required_keys and key not in optional_keys:
                        print(f"Undefined Key: {key} does not exist in the required keys list for {post.url}")

                for attachment_key in post.data["attachment"]:
                    if attachment_key not in attachment_keys:
                        print(f"Undefined Attachment Key: {attachment_key} does not exist in the attachment keys list for {post.url}")

                if post.data["membershipOnly"] == True:
                    print(f"Key: membershipOnly is True in {post.url}")

                if post.data["hasProduct"] == True:
                    print(f"Key: hasProduct is True in {post.url}")

                if post.data["locked"] == True:
                    print(f"Key: locked is True in {post.url}")

                if post.data["postType"] != "NORMAL":
                    print(f"Key: postType is not NORMAL in {post.url}")

                if post.data["extension"]:
                    print(f"Key: extension is not empty in {post.url}")

            start = False
            loop += 1"""


class LegacyTests:
    sunverse_client = SunverseClient("", "")

    @pytest.mark.asyncio
    async def test_fetch_community(self, mocker):
        """This test is to ensure that the :class:`sunverse.objects.Community`
        object is able to be created successfully.

        Notes
        -----
        The data used for testing this method is mocked. As such, no API calls
        will be made when this test executes.
        """
        with open("tests/test_community.json", encoding="utf-8") as file:
            community_data = json.load(file)

        mocker.patch(
            "sunverse.sunverse.SunverseClient.fetch_community",
            return_value=Community(community_data),
        )

        community = await self.sunverse_client.fetch_community(1029)
        assert community == Community(community_data)

    @pytest.mark.asyncio
    async def test_fetch_artists(self, mocker):
        """This test is to ensure that the :class:`sunverse.objects.Artist`
        object is able to be created successfully.

        Notes
        -----
        The data used for testing this method is mocked. As such, no API calls
        will be made when this test executes.
        """

        with open("tests/test_artists.json", encoding="utf-8") as file:
            artist_data = json.load(file)

        mocker.patch(
            "sunverse.sunverse.SunverseClient.fetch_artists",
            return_value={data["memberId"]: Artist(data, 1029) for data in artist_data},
        )

        artists = await self.sunverse_client.fetch_artists(1029)
        assert artists == Artist(artist_data, 1029)

    @pytest.mark.asyncio
    async def test_fetch_notification(self, mocker):
        """This test is to ensure that the :class:`sunverse.objects.Notification`
        object is able to be created successfully.

        Notes
        -----
        The data used for testing this method is mocked. As such, no API calls
        will be made when this test executes.
        """
        with open("tests/test_notification.json", encoding="utf-8") as file:
            notification_data = json.load(file)

        mocker.patch(
            "sunverse.sunverse.SunverseClient.fetch_notification",
            return_value=Notification(notification_data),
        )

        notification = await self.sunverse_client.fetch_notification(1576070310486122793)
        assert notification == Notification(notification_data)
