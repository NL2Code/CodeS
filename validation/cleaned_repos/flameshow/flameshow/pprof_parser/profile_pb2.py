"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\rprofile.proto\x12\x12perftools.profiles"\xd5\x03\n\x07Profile\x12\x32\n\x0bsample_type\x18\x01 \x03(\x0b\x32\x1d.perftools.profiles.ValueType\x12*\n\x06sample\x18\x02 \x03(\x0b\x32\x1a.perftools.profiles.Sample\x12,\n\x07mapping\x18\x03 \x03(\x0b\x32\x1b.perftools.profiles.Mapping\x12.\n\x08location\x18\x04 \x03(\x0b\x32\x1c.perftools.profiles.Location\x12.\n\x08\x66unction\x18\x05 \x03(\x0b\x32\x1c.perftools.profiles.Function\x12\x14\n\x0cstring_table\x18\x06 \x03(\t\x12\x13\n\x0b\x64rop_frames\x18\x07 \x01(\x03\x12\x13\n\x0bkeep_frames\x18\x08 \x01(\x03\x12\x12\n\ntime_nanos\x18\t \x01(\x03\x12\x16\n\x0e\x64uration_nanos\x18\n \x01(\x03\x12\x32\n\x0bperiod_type\x18\x0b \x01(\x0b\x32\x1d.perftools.profiles.ValueType\x12\x0e\n\x06period\x18\x0c \x01(\x03\x12\x0f\n\x07\x63omment\x18\r \x03(\x03\x12\x1b\n\x13\x64\x65\x66\x61ult_sample_type\x18\x0e \x01(\x03"\'\n\tValueType\x12\x0c\n\x04type\x18\x01 \x01(\x03\x12\x0c\n\x04unit\x18\x02 \x01(\x03"V\n\x06Sample\x12\x13\n\x0blocation_id\x18\x01 \x03(\x04\x12\r\n\x05value\x18\x02 \x03(\x03\x12(\n\x05label\x18\x03 \x03(\x0b\x32\x19.perftools.profiles.Label"@\n\x05Label\x12\x0b\n\x03key\x18\x01 \x01(\x03\x12\x0b\n\x03str\x18\x02 \x01(\x03\x12\x0b\n\x03num\x18\x03 \x01(\x03\x12\x10\n\x08num_unit\x18\x04 \x01(\x03"\xdd\x01\n\x07Mapping\x12\n\n\x02id\x18\x01 \x01(\x04\x12\x14\n\x0cmemory_start\x18\x02 \x01(\x04\x12\x14\n\x0cmemory_limit\x18\x03 \x01(\x04\x12\x13\n\x0b\x66ile_offset\x18\x04 \x01(\x04\x12\x10\n\x08\x66ilename\x18\x05 \x01(\x03\x12\x10\n\x08\x62uild_id\x18\x06 \x01(\x03\x12\x15\n\rhas_functions\x18\x07 \x01(\x08\x12\x15\n\rhas_filenames\x18\x08 \x01(\x08\x12\x18\n\x10has_line_numbers\x18\t \x01(\x08\x12\x19\n\x11has_inline_frames\x18\n \x01(\x08"v\n\x08Location\x12\n\n\x02id\x18\x01 \x01(\x04\x12\x12\n\nmapping_id\x18\x02 \x01(\x04\x12\x0f\n\x07\x61\x64\x64ress\x18\x03 \x01(\x04\x12&\n\x04line\x18\x04 \x03(\x0b\x32\x18.perftools.profiles.Line\x12\x11\n\tis_folded\x18\x05 \x01(\x08")\n\x04Line\x12\x13\n\x0b\x66unction_id\x18\x01 \x01(\x04\x12\x0c\n\x04line\x18\x02 \x01(\x03"_\n\x08\x46unction\x12\n\n\x02id\x18\x01 \x01(\x04\x12\x0c\n\x04name\x18\x02 \x01(\x03\x12\x13\n\x0bsystem_name\x18\x03 \x01(\x03\x12\x10\n\x08\x66ilename\x18\x04 \x01(\x03\x12\x12\n\nstart_line\x18\x05 \x01(\x03\x42-\n\x1d\x63om.google.perftools.profilesB\x0cProfileProtob\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "profile_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = (
        b"\n\035com.google.perftools.profilesB\014ProfileProto"
    )
    _PROFILE._serialized_start = 38
    _PROFILE._serialized_end = 507
    _VALUETYPE._serialized_start = 509
    _VALUETYPE._serialized_end = 548
    _SAMPLE._serialized_start = 550
    _SAMPLE._serialized_end = 636
    _LABEL._serialized_start = 638
    _LABEL._serialized_end = 702
    _MAPPING._serialized_start = 705
    _MAPPING._serialized_end = 926
    _LOCATION._serialized_start = 928
    _LOCATION._serialized_end = 1046
    _LINE._serialized_start = 1048
    _LINE._serialized_end = 1089
    _FUNCTION._serialized_start = 1091
    _FUNCTION._serialized_end = 1186
# @@protoc_insertion_point(module_scope)
