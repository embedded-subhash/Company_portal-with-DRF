from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from api.responses import SuccessResponse


class StandardResponseModelViewSet(ModelViewSet):
    create_message = "Created Successfully"
    update_message = "Updated Successfully"
    delete_message = "Deleted Successfully"
    list_message = "Records Fetched Successfully"
    retrieve_message = "Record Fetched Successfully"

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            self.paginator.message = self.list_message
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(self.list_message, serializer.data)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return SuccessResponse(self.retrieve_message, serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_service_create(serializer.validated_data)
        output_serializer = self.get_serializer(instance)
        return SuccessResponse(
            self.create_message,
            output_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        instance = self.perform_service_update(instance, serializer.validated_data)
        output_serializer = self.get_serializer(instance)
        return SuccessResponse(self.update_message, output_serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_service_delete(instance)
        return SuccessResponse(
            self.delete_message,
            {},
            status=status.HTTP_200_OK,
        )

    def perform_service_create(self, validated_data):
        serializer = self.get_serializer(data=validated_data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def perform_service_update(self, instance, validated_data):
        serializer = self.get_serializer(instance, data=validated_data, partial=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def perform_service_delete(self, instance):
        instance.delete()
